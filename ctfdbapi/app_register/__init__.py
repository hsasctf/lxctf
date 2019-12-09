import random
import string

import flask
from flask import Flask, json, jsonify, request
from flask import render_template
from flask_mail import Message, Mail
from sqlalchemy import func

from app_register.utils import is_safe_url
from db.database import db_session
from flask_httpauth import HTTPBasicAuth

from db.models import Team
from flask import Blueprint, render_template, abort, request, jsonify, current_app
from flask import flash
from flask import json
from jinja2 import TemplateNotFound
from hashlib import sha512
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g

from db.database import db_session
from db.models import TeamScore, AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, \
    Tick, TeamServiceState, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun

from hashlib import sha512

import redis
import requests
from app_register import config
from sqlalchemy.orm import Query
from datetime import datetime
from ipaddress import ip_address, ip_network

from app_register.forms import RegistrationForm, LoginForm, PasswordResetForm, UnregisterForm, AttendForm
from hash_passwort import generate_password


app = Flask(__name__, template_folder='templates', static_url_path="/static")

app.config.from_object(config)
mail = Mail()
mail.init_app(app)
login_manager = LoginManager()



#### Register
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# gets the ip adress
def get_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR'].lstrip("::ffff:")

#checkig if the person is outside of the university network
@app.before_request
def limit_remote_addr():
    print(get_ip())
    if not any(ip_address(get_ip()) in ip_network(x) for x in config.ALLOWED_IP_RANGES):
        return "not available outside of university network", 403


@login_manager.user_loader
def load_user(user_id):
    return Team.query.filter_by(id=int(user_id)).first()


# validate a Team and adds the Team later in the DB
@app.route("/validate/<token>")
def validate(token):
    u = Team.query.filter_by(token=token).first()
    u.verified = datetime.now()
    u.save()
    db_session.commit()


# gives you the route to the /faq page
@app.route("/faq/")
def faq():
    return render_template("faq.html")

# gives you the route to the home html side with the name "index.html"
@app.route("/")
def index():
    event = get_empty_event_or_fail()
    return render_template("index.html", event=event)

# Dominik
@app.route("/validation_unregister/<token>/")
def validation_unregister(token):
    if len(token) < 10:
        flash("Error")
    user = User.query.filter_by(token=token).first()
    if not user:
        flash("Error")
    else:
        #members = Member.query.filter_by(user=user).delete()
        db_session.delete(user)
        db_session.commit()
        flash("Success")
    return flask.redirect(flask.url_for('index'))


# Here we have the possibility that a Person can unregister his Account
@app.route('/unregister/', methods=['GET', 'POST'])
def unregister():
    # Checks if the User is loged in
    if current_user.is_authenticated:
        flash("Please logout to use the unregister function.")
        return redirect(url_for('index'))
    form = UnregisterForm()
    # Checks if the button is pushed and than checks if the E-Mail is right
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("Email address not found")
            return flask.redirect(flask.url_for('unregister'))

        user.ensure_token()
        db_session.commit()

        msg = Message(subject="Unregister",
                      sender="ctf@nohost.eu",
                      reply_to="register@ctf.uber.space",
                      recipients=[user.email],
                      body="You requested your deletion from all CTF teams. To confirm use this URL"
                           " {}{}".format(
                        config.URL_BASE,
                        url_for("validation_unregister", token=user.token)),
                      )
        mail.send(msg)
        flash("Email was sent to your email address. Please follow the instructions in this email.")

    return flask.render_template('unregister.html', form=form)


@app.route("/validation_user/<token>/") # ???


@app.route("/validate.php", defaults={'token': None})  # TODO testk
def validation_user(token):
    # checks if there is a token there if not give an error
    if token is None:
        token = request.args.get('token')
        if not token:
            flash("error")
        print(token)

    # Verify the email address with the datetime
    user = User.query.filter_by(token=token).first()
    if user:
        user.verified = datetime.now()
        db_session.commit()
        flash("Successfully verified email address")
    else:
        flash("Token not found")

    return flask.redirect(flask.url_for('index'))


# displays the team that are competing
@app.route('/teams/', methods=['GET'])
def teams():
    events = Event.query.filter_by().order_by(Event.id.desc())
    return flask.render_template('teams.html', events=events)
    
# function how to create a team
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    # checks if there is a team name
    if form.validate_on_submit():
        team = Team.query.filter_by(team_name=form.teamname.data).first()
        if team is not None:
            flash('Invalid teamname')
            return redirect(url_for('register'))
        # takes a teamname and a password for the team and than put it in the db
        t = Team()
        t.set_password(form.password.data)
        t.team_name = form.teamname.data
        db_session.add(t)
        db_session.commit()
        flash("Team is now registered. You can now log in")
        return flask.redirect(flask.url_for('login'))


    return flask.render_template('register.html', form=form)

# function how to login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # checks if ether the pwd or the name is wrong
    if form.validate_on_submit():
        user = Team.query.filter_by(team_name=form.teamname.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)

        flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)
        print(str(next))
        return flask.redirect(next or flask.url_for('index'))

    return flask.render_template('login.html', form=form)

# Here you see how your password is reseted
@app.route("/validation_passwordreset/<team_id>/<hash>/")
def validation_passwordreset(team_id, hash):
    # gets the value=id from the db
    team = Team.query.filter_by(id=int(team_id)).first()

    # if there is no such id than there is no team
    if not team:
        flash("Team not found")

    # if there is a team than change the password and send it trough an email to the user
    else:
        if hash == team.password:
            members = Member.query.filter_by(team=team)
            users = [m.user for m in members]

            pw = generate_password(length=9)
            team.set_password(pw)
            db_session.commit()

            msg = Message(subject="Password Reset",
                          sender="ctf@nohost.eu",
                          reply_to="register@ctf.uber.space",
                          recipients=[u.email for u in users],
                          body="Password for your team was set to: {}".format(pw)
                          )
            mail.send(msg)

            flash('Email with new password was sent to all team members')
        else:
            flash("Incorrect Token")

    return flask.redirect(flask.url_for('index'))

# this step happens before the above?
# Here your password is reset by the user
@app.route('/passwordreset/', methods=['GET', 'POST'])
def passwordreset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetForm()
    # gets the team data from the db and sends an email
    if form.validate_on_submit():
        team = form.teamname.data
        team_id = team.id
        team = Team.query.filter_by(id=team_id).first()
        members = Member.query.filter_by(team=team)
        users = [m.user for m in members]

        msg = Message(subject="Password Reset",
                      sender="ctf@nohost.eu",
                      reply_to="register@ctf.uber.space",
                      recipients=[u.email for u in users],
                      body="Please validate your password reset request at {}{}".format(
                        config.URL_BASE,
                        url_for("validation_passwordreset", team_id=team.id, hash=team.password)),
                      )
        mail.send(msg)

        flash('Email was sent to all team members')



    return flask.render_template('passwordreset.html', form=form)

# returns you the first free subnet
def first_empty_subnet():
    event = get_empty_event_or_fail()
    attending_teams = AttendingTeam.query.filter_by(event=event)
    used_nets = {a.subnet for a in attending_teams}
    free_nets = set(range(1,250)).difference(used_nets)
    return list(free_nets)[0]

# checks if there is already an event existing or if the user has to create a new one
def get_empty_event_or_fail():
    event = Event.query.order_by(Event.id.desc()).first()
    if event.ticks.first():
        raise Exception("Cannot use an event with existing ticks. Create a new event.")
    return event



# sends a validation email to the team user
def send_validation_email(u, team):
    msg = Message(subject="Confirm your registration in CTF team",
                  sender="ctf@nohost.eu",
                  reply_to="register@ctf.uber.space",
                  recipients=[u.email],
                  body="You were added to the CTF team *{}*. To confirm your membership use this URL"
                       " {}{}".format(
                      team.team_name,
                      config.URL_BASE,
                      url_for("validation_user", token=u.token)),
                  )
    mail.send(msg)

# if the vaildation email failed than there is a retry
@app.route("/retry_validation/<user_id>/", methods=['POST'])
@login_required
def retry_validation(user_id):
    team = current_user
    user = User.query.filter_by(id=int(user_id)).first()
    
    # test if validation is allowed
    if not Member.query.filter_by(team=team, user=user).first():
        return "ERROR"
    
    send_validation_email(user, team)
    
    flash("New validation email was sent to user")
    
    return redirect(url_for("index"))




@app.route("/attend/", methods=['GET', 'POST'])
@login_required
def attend():
    team = current_user
    event = get_empty_event_or_fail()
    attending = AttendingTeam.query.filter_by(event=event, team=team).first()

    form = AttendForm()
    if form.validate_on_submit():
        members_to_add = []

        # checks if there is a tuple that is there from with the memeber
        def verify_member_form(tpl):
            if any(tpl):
                if not all(tpl):
                    return False
                return True
            return None

        # checks if all the fields are filled mith input
        def check_3_tuple(tpl):
            tpl = tuple(t.strip() for t in tpl)
            if verify_member_form(tpl) is False:
                flash("Fill all 3 fields for each member")
                return False
                #return flask.render_template('attend.html', form=form, members=team.members, attending=attending)
            
            # checks if a university is used  --> hard coded
            elif verify_member_form(tpl) is True:
                if not tpl[0].endswith("@hs-albsig.de"): # FIXME
                    flash("Please use only university email addresses")
                    return False
                    #return flask.render_template('attend.html', form=form, members=team.members, attending=attending)
                members_to_add.append(tpl)
            else:
                print("Empty 3-tuple")
            return True
        # Check form

        _ = check_3_tuple((form.email1.data, form.surname1.data, form.forename1.data))
        if not _:
            return flask.render_template('attend.html', form=form, members=team.members, attending=attending)
        _ = check_3_tuple((form.email2.data, form.surname2.data, form.forename2.data))
       	if not _:
       	    return flask.render_template('attend.html', form=form, members=team.members, attending=attending)
        _ = check_3_tuple((form.email3.data, form.surname3.data, form.forename3.data))
       	if not _:
       	    return flask.render_template('attend.html', form=form, members=team.members, attending=attending)
        _ = check_3_tuple((form.email4.data, form.surname4.data, form.forename4.data))
       	if not _:
       	    return flask.render_template('attend.html', form=form, members=team.members, attending=attending)
        _ = check_3_tuple((form.email5.data, form.surname5.data, form.forename5.data))
       	if not _:
       	    return flask.render_template('attend.html', form=form, members=team.members, attending=attending)

        # delete AttendingTeam
        if attending is not None:
            db_session.delete(attending)
            db_session.commit()

        # delete all users
        for m in team.members:
            db_session.delete(m.user)
            db_session.delete(m)
        db_session.commit()

        # first checks if there are user registerd  then deletes
        for email, surname, forename in members_to_add:
            test_u = User.query.filter_by(email=email).first()
            if test_u is not None:
                flash("User with this email found in database. Please unregister first.")
                return flask.render_template('attend.html', form=form, members=team.members, attending=attending)
            else:
                u = User()
                u.email = email
                u.surname = surname
                u.forename = forename
                u.ensure_token()
                db_session.add(u)

                m = Member()
                m.team = team
                m.user = u
                db_session.add(m)
                db_session.commit()

                send_validation_email(u, team)

        # add AttendingTeam if member count is > 0
        if len(members_to_add) > 0:
            at = AttendingTeam()
            at.event = event
            at.team = team
            at.subnet = first_empty_subnet()
            db_session.add(at)
            db_session.commit()
            flash("Emails were sent to your email addresses. Please follow the instructions in this email.")



        db_session.commit()

        return flask.redirect(flask.url_for('attend'))

        # Send verification links TODO


    return flask.render_template('attend.html', form=form, members=team.members, attending=attending)



# logout from the user
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
