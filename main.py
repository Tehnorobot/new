from data import db_session, api
from data.users import User
from data.jobs import Jobs
from flask import Flask, url_for, request, render_template, redirect, abort
import datetime
from flask_restful import abort, Api
from flask_login import LoginManager, login_manager, login_required, login_user, logout_user, current_user
from forms.user import LoginForm, RegisterForm
from forms.job import JobAddForm
from data import jobs_resource, users_resource

db_session.global_init("db/blogs.db")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

app.register_blueprint(api.blueprint)

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resource.JobResource, '/api/v2/jobs/<int:job_id>')

api.add_resource(users_resource.UserListResource, '/api/v2/users')
api.add_resource(users_resource.UserResource, '/api/v2/users/<int:user_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    params = {}
    params["title"] = "Журнал работ"
    params["static_css"] = url_for('static', filename="css/")
    params["static_img"] = url_for('static', filename="img/")
    params["jobs"] = session.query(Jobs).all()
    return render_template('index.html', **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    params = {}
    params["title"] = "Авторизация"
    params["static_css"] = url_for('static', filename="css/")
    params["static_img"] = url_for('static', filename="img/")

    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, **params)
    return render_template('login.html', form=form, **params)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    params = {}
    params["title"] = "Регистрация"
    params["static_css"] = url_for('static', filename="css/")
    params["static_img"] = url_for('static', filename="img/")

    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', **params,
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', **params,
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', **params, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addJob():
    params = {}
    params["title"] = "Добавление работы"
    params["static_css"] = url_for('static', filename="css/")
    params["static_img"] = url_for('static', filename="img/")

    form = JobAddForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.id == form.teamLeader.data).first():
            return render_template('addJob.html', **params,
                                   form=form,
                                   message="Такого team leader нет")
        job = Jobs(
            team_leader=form.teamLeader.data,
            job=form.title.data,
            work_size=form.workSize.data,
            collaborators=form.collaborators.data,
            if_finished=form.complete.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addJob.html', **params, form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job:
        if current_user.id != job.team_leader and current_user.id != 1:
            return "Нет прав"
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    params = {}
    params["title"] = "Редактирование работы"
    params["static_css"] = url_for('static', filename="css/")
    params["static_img"] = url_for('static', filename="img/")
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if not job:
        abort(404)
    if current_user.id != job.team_leader and current_user.id != 1:
        return "Нет прав"
    form = JobAddForm()
    if request.method == "GET":
        form.teamLeader.data = job.team_leader
        form.title.data = job.job
        form.workSize.data = job.work_size
        form.collaborators.data = job.collaborators
        form.complete.data = job.if_finished
    if form.validate_on_submit():
        if not db_sess.query(User).filter(User.id == form.teamLeader.data).first():
            return render_template('addJob.html', **params,
                                   form=form,
                                   message="Такого team leader нет")
        job.team_leader = form.teamLeader.data
        job.job = form.title.data
        job.work_size = form.workSize.data
        job.collaborators = form.collaborators.data
        job.if_finished = form.complete.data
        db_sess.commit()
        return redirect('/')

    return render_template('addJob.html',
                           **params,
                           form=form
                           )


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=8080, host='0.0.0.0')
