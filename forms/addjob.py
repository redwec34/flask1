import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    team_leader = IntegerField('ID ответственного', validators=[DataRequired()])
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Время выполнения в часах', validators=[DataRequired()])
    collaborators = StringField('Список id исполнителей', validators=[DataRequired()])
    start_date = DateTimeField('Дата начала', default=datetime.datetime.now(),
                               format='%Y-%m-%d %H:%M:%S')
    end_date = DateTimeField('Дата окончания', default=datetime.datetime.now(),
                             format='%Y-%m-%d %H:%M:%S')
    is_finished = BooleanField('Закончена ли?')
    submit = SubmitField('Добавить работу')