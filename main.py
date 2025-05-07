from flask import Flask, render_template, redirect
from registerform import RegForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/register', methods=['GET', 'POST'])
def login():
    form = RegForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('reg.html', form=form)


if __name__ == '__main__':
    app.run()
