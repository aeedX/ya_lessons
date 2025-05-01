from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

@app.route('/gallery', methods=['POST', 'GET'])
def gallery():
    if request.method == 'GET':
        files = list(os.listdir('static/img'))
        return render_template('gallery.html', n=len(files), filenames=files)
    elif request.method == 'POST':
        f = request.files['file']
        f.save(f'static/img/{f.filename}')
        return redirect('/gallery')


if __name__ == '__main__':
    app.run()
