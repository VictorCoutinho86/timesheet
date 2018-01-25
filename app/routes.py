from app import app, db
from app.models import Usuario
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Pagina Inicial')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Usuário ou senha incorretos')
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            flash('Usuário ou senha incorretos')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Entre', form=form)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Usuario(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registre-se', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = Usuario.query.filter_by(username=username).first_or_404()
    if user.username != current_user.username:
        flash("You can't see the profile of others users!")
        return redirect(url_for('user'))
    return render_template('user.html', user=user)


@app.route('/index')
@login_required
def index():
    return "Olá {}".format(current_user.username)
