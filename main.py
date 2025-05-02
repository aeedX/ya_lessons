from json import load

from flask import Flask, render_template
from random import choice

app = Flask(__name__)

@app.route('/member')
def member():
    with open('templates/members.json', 'r', encoding="UTF8") as f:
        return render_template('member.html', member=choice(load(f)))


if __name__ == '__main__':
    app.run()
