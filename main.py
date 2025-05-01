from flask import Flask, render_template
import os

app = Flask(__name__)
img = None

@app.route('/table_param/<sex>/<int:age>')
def table(sex, age):
    return render_template('table.html', sex=sex, age=age)


if __name__ == '__main__':
    app.run()
