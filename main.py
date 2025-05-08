from flask import Flask, render_template, redirect
from forms import *
from data.__all_models import *
import datetime as dt
from data import db_session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def works():
    db_sess = db_session.create_session()
    works = db_sess.query(Jobs)
    return render_template('works.html', works=works, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit() and form.password.data == form.password_confirm.data:
        db_sess = db_session.create_session()
        user = User()
        user.email = form.email.data
        user.set_password(form.password.data)
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('reg.html', title='Регистрация', form=form, current_user=current_user)


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
    return render_template('login.html', title='Авторизация', form=form, current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Adding a Job', form=form, current_user=current_user)


@app.route('/editjob/<int:jobs_id>', methods=['GET', 'POST'])
@login_required
def edit_job(jobs_id):
    form = JobForm()
    if form.validate_on_submit():
        if form.team_leader.data == current_user.id or current_user.id == 1:
            db_sess = db_session.create_session()
            job = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
            if job:
                job.team_leader = form.team_leader.data
                job.job = form.job.data
                job.work_size = form.work_size.data
                job.collaborators = form.collaborators.data
                job.is_finished = form.is_finished.data
                db_sess.commit()
            return redirect('/')
        else:
            return render_template('addjob.html', message="нет доступа",
                                   title='Edit a Job', form=form, current_user=current_user)
    return render_template('addjob.html', title='Edit a Job', form=form, current_user=current_user)


@app.route('/deljob/<int:jobs_id>', methods=['GET', 'POST'])
@login_required
def del_job(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    if job and (job.team_leader == current_user.id or current_user.id == 1):
        db_sess.delete(job)
        db_sess.commit()
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init("db/data.db")
    app.run()
