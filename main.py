from flask import Flask, render_template, request, redirect
from loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
form = {}

@app.route('/auto_answer', methods=['GET', 'POST'])
def auto_answer():
    if request.method == 'GET':
        return render_template('auto_answer.html')
    elif request.method == 'POST':
        form['surname'] = request.form['surname']
        form['name'] = request.form['name']
        form['email'] = request.form['email']
        form['edu'] = request.form['edu']
        form['prof'] = request.form.getlist('prof')
        form['sex'] = request.form['sex']
        form['about'] = request.form['about']
        form['accept'] = bool(request.form['accept'])
        return redirect('/answer')


@app.route('/answer')
def answer():
    return render_template('answer.html', form=form)


if __name__ == '__main__':
    app.run()
