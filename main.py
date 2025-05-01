from flask import Flask, render_template
import os

app = Flask(__name__)
img = None

@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', prof='eng' if ('инженер' in prof or 'строитель in prof') else 'sc')


if __name__ == '__main__':
    app.run()
