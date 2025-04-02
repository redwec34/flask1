from flask import Flask, redirect, render_template

app = Flask(__name__)


@app.route('/<title>')
@app.route('/index/<title>')
def index1(title):
    return render_template("index.html", title=title)


@app.route('/training/<prof>')
def train(prof):
    return render_template('index.html', title='Тренировки', prof=prof.lower())


@app.route('/list_prof/<list>')
def index2(list):
    proff = [
    "инженер-исследователь",
    "пилот",
    "строитель",
    "экзобиолог",
    "врач",
    "инженер по терраформированию",
    "климатолог",
    "специалист по радиационной защите",
    "астрогеолог",
    "гляциолог",
    "инженер жизнеобеспечения",
    "метеоролог",
    "оператор марсохода",
    "киберинженер",
    "штурман",
    "пилот дронов"
]
    return render_template("index.html", list=list, prof=proff)


@app.route('/distribution')
def distribution():
    astronauts = [
        "Ридли Скотт",
        "Энди Уир",
        "Марк Уотни",
        "Венката Капур",
        "Тедди Сандерс",
        "Шон Бин"
    ]
    return render_template('index.html', astronauts=astronauts)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')