from flask import render_template, url_for, flash, redirect, request
from albsigbank import app, db, bcrypt
from albsigbank.forms import RegistrationForm, LoginForm, NoteForm
from albsigbank.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_basicauth import BasicAuth
import re

app.config['BASIC_AUTH_USERNAME'] = 'employee'
app.config['BASIC_AUTH_PASSWORD'] = 'changeme'

basic_auth = BasicAuth(app)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/quickaccess")
@basic_auth.required
def quickaccess():
    user = User.query.filter_by(username="admin").first()
    return render_template('quickaccess.html', notes=user.notes)    

@app.route("/account", methods=['GET', 'POST'])
@app.route("/account/", methods=['GET', 'POST'])
@login_required
def account():
    if re.match("admin", current_user.username):
        form = NoteForm()
        user = User.query.filter_by(username="admin").first()
        if form.validate_on_submit():
            if len(user.notes) > 1024:
                user.notes = ''
                flash('You reached the limit of the notepad size. All notes where deleted.')
            user.notes = user.notes + ' •' +  form.notes.data
            db.session.commit()
        return render_template('account_admin.html', form=form, notes=user.notes)
    else:
        return render_template('account_dashboard.html')

@app.route("/account/contact")
@login_required
def contact():
    if re.match("admin", current_user.username):
         return redirect(url_for('account'))
    else:
        return render_template('account_contact.html')

@app.route("/account/notes", methods=['GET', 'POST'])
@login_required
def notes():
    form = NoteForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if len(user.notes) > 1024:
            user.notes = ''
            flash('You reached the limit of the notepad size. All notes where deleted.')
        user.notes = user.notes + ' •' +  form.notes.data
        db.session.commit()
    if re.match("admin", current_user.username):
        return redirect(url_for('account'))
    else:
        return render_template('account_notes.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, notes=' ')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/adminoffice")
def adminoffice():
    user = User.query.filter_by(username="admin").first()
    return render_template('adminoffice.html', notes=user.notes)
