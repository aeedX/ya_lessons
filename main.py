from flask import Flask, render_template, redirect, make_response, jsonify
import requests
from forms import *
from data.__all_models import *
from data import db_session, users_api
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def works():
    db_sess = db_session.create_session()
    works = db_sess.query(Jobs)
    return render_template('works.html', works=works, current_user=current_user)


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department)
    return render_template('departments.html', departments=departments, current_user=current_user)


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
        job.category_id = form.category_id.data
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
                job.category_id = form.category_id.data
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


@app.route('/adddepartment', methods=['GET', 'POST'])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.chief = form.chief.data
        department.title = form.title.data
        department.email = form.email.data
        department.members = form.members.data
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('adddepartment.html', title='Adding a Department', form=form, current_user=current_user)


@app.route('/editdepartment/<int:department_id>', methods=['GET', 'POST'])
@login_required
def edit_department(department_id):
    form = DepartmentForm()
    if form.validate_on_submit():
        if form.chief.data == current_user.id or current_user.id == 1:
            db_sess = db_session.create_session()
            department = db_sess.query(Department).filter(Department.id == department_id).first()
            if department:
                department.chief = form.chief.data
                department.title = form.title.data
                department.email = form.email.data
                department.members = form.members.dataa
                db_sess.commit()
            return redirect('/departments')
        else:
            return render_template('adddepartment.html', message="нет доступа",
                                   title='Edit a Department', form=form, current_user=current_user)
    return render_template('adddepartment.html', title='Edit a Department', form=form, current_user=current_user)


@app.route('/deldepartment/<int:department_id>', methods=['GET', 'POST'])
@login_required
def del_department(department_id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == department_id).first()
    if department and (department.chief == current_user.id or current_user.id == 1):
        db_sess.delete(department)
        db_sess.commit()
    return redirect('/department')


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    db_sess = db_session.create_session()
    user = requests.get(f'http://localhost:5000/api/users/{user_id}').json()
    pos = requests.get(f'http://geocode-maps.yandex.ru/1.x/?geocode={user.city_from}&format=json&apikey=8013b162-6b42-4997-9691-77b7074026e0').json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].replace(' ', ',')
    img = f"https://static-maps.yandex.ru/v1?ll={pos}&z=12&apikey=f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
    return render_template('users_show.html', user=user, img=img, current_user=current_user)


if __name__ == '__main__':
    db_session.global_init("db/data.db")
    app.register_blueprint(users_api.blueprint)
    app.run()
