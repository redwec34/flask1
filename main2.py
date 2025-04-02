from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import Api

from data import db_session, users_resource
from data.users import User
from data.jobs import Jobs

from forms.login import LoginForm
from forms.register import RegisterForm
from forms.addjob import AddJobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/mars_explorer.db")
app = Flask(__name__)
api = Api(app)
api.add_resource(users_resource.UsersListResource, '/api/v2/news')
api.add_resource(users_resource.UsersResource, '/api/v2/news/<int:news_id>')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    names = dict()
    for job in jobs:
        user = db_sess.query(User).filter(User.id == job.team_leader).first()
        names[job.team_leader] = user.surname + ' ' + user.name
    return render_template("index.html", jobs=jobs, names=names, title="Марсиане")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_repeat.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    new_job = AddJobForm()
    if new_job.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.id == new_job.team_leader.data).all():
            return render_template('addjob.html',
                                   title='Добавление работы', form=new_job,
                                   message="ID ответственного нет в БД")
        jobs = Jobs(
            job=new_job.job.data,
            team_leader=new_job.team_leader.data,
            work_size=new_job.work_size.data,
            collaborators=new_job.collaborators.data,
            is_finished=new_job.is_finished.data,
            start_date=new_job.start_date.data,
            end_date=new_job.end_date.data
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Добавление работы', form=new_job)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = AddJobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.user == current_user) | (current_user.id == 1)
                                          ).first()
        if jobs:
            form.job.data = jobs.job
            form.team_leader.data = jobs.team_leader
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
            form.start_date.data = jobs.start_date
            form.end_date.data = jobs.end_date
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.user == current_user) | (current_user.id == 1)
                                          ).first()
        if jobs:
            jobs.job = form.job.data
            jobs.team_leader = form.team_leader.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            jobs.start_date = form.start_date.data
            jobs.end_date = form.end_date.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      (Jobs.user == current_user) | (current_user.id == 1)
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')