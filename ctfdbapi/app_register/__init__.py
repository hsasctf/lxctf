import os

import flask
from flask_mail import Message, Mail

from app_register.utils import is_safe_url

from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g
from flask import send_file, send_from_directory, safe_join

from db.database import db_session
from db.models import AttendingTeam, Event, Team, Member, User

from app_register import config
from datetime import datetime
from ipaddress import ip_address, ip_network

from app_register.forms import RegistrationForm, LoginForm, PasswordResetForm, UnregisterForm, AttendForm
from manage_hash_password import generate_password

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


def get_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR'].lstrip("::ffff:")


@app.before_request
def limit_remote_addr():
    print(get_ip())
    if not any(ip_address(get_ip()) in ip_network(x) for x in config.ALLOWED_IP_RANGES):
        return "not available outside of university network", 403


@login_manager.user_loader
def load_user(user_id):
    return Team.query.filter_by(id=int(user_id)).first()


# TODO this is unused code?
@app.route("/validate/<token>")
def validate(token):
    u = Team.query.filter_by(token=token).first()
    u.verified = datetime.now()
    u.save()
    db_session.commit()


@app.route("/faq/")
def faq():
    return render_template("faq.html")


@app.route("/")
def index():
    try:
        event = get_empty_event_or_fail()
    except:
        return "Database error, there is no empty event in database (event without ticks)"
    return render_template("index.html", event=event)


@app.route("/validation_unregister/<token>/")
def validation_unregister(token):
    if len(token) < 10:
        flash("Error")
    user = User.query.filter_by(token=token).first()
    if not user:
        flash("Error")
    else:
        # members = Member.query.filter_by(user=user).delete()
        db_session.delete(user)
        db_session.commit()
        flash("Success")
    return flask.redirect(flask.url_for('index'))


@app.route('/unregister/', methods=['GET', 'POST'])
def unregister():
    if current_user.is_authenticated:
        flash("Please logout to use the unregister function.")
        return redirect(url_for('index'))
    form = UnregisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("Email address not found")
            return flask.redirect(flask.url_for('unregister'))

        user.ensure_token()
        db_session.commit()

        msg = Message(subject="Unregister",
                      sender=config.MAIL_DEFAULT_SENDER,
                      reply_to=config.MAIL_REPLY_TO,
                      recipients=[user.email],
                      body="You requested your deletion from all CTF teams. To confirm use this URL"
                           " {}{}".format(
                          config.URL_BASE,
                          url_for("validation_unregister", token=user.token)),
                      )
        mail.send(msg)
        flash("Email was sent to your email address. Please follow the instructions in this email.")

    return flask.render_template('unregister.html', form=form)


@app.route("/validation_user/<token>/")
def validation_user(token):
    if token is None:
        token = request.args.get('token')
        if not token:
            flash("error")
        print(token)

    user = User.query.filter_by(token=token).first()
    if user:
        user.verified = datetime.now()
        db_session.commit()
        flash("Successfully verified email address")
    else:
        flash("Token not found")

    return flask.redirect(flask.url_for('index'))


@app.route('/download/', methods=['GET'])
def download():
    """
    this function is needed for providing log in keys while the game is running
    """
    team = current_user
    event = Event.query.order_by(Event.id.desc()).first()
    # use event.start here, not event.attack_defense_start
    # event.start is when teams should log in to patch services
    running = event.start < datetime.now() < event.end
    attending = AttendingTeam.query.filter_by(event=event, team=team).first()

    return flask.render_template('download.html', attending=attending, running=running)


@app.route('/download_file/<name>/', methods=['GET'])
def download_type(name):
    """
    provide download for VPN and ssh keys
    """
    team = current_user
    event = Event.query.order_by(Event.id.desc()).first()
    # use event.start here, not event.attack_defense_start
    # event.start is when teams should log in to patch services
    running = event.start < datetime.now() < event.end
    if not running:
        return "Download only works during event"
    if name not in ["wg1", "wg2", "wg3", "wg4", "wg5", "ovpn", "ssh"]:
        return "unknown file type"
    attending = AttendingTeam.query.filter_by(event=event, team=team).first()
    subnet = attending.subnet
    ar_path = os.path.dirname(os.path.realpath(__file__))
    vpn = os.path.join(ar_path, "..", "..", "roles", "vpn", "files", "client_configs")
    ssh = os.path.join(ar_path, "..", "..", "roles", "infrastructure_lxd", "files", "team_keys")

    if name == "ovpn":
        return send_from_directory(vpn, filename="client-team{}.ovpn".format(int(subnet)), as_attachment=True)
    elif name.startswith("wg"):
        num = int(name.lstrip("wg"))
        return send_from_directory(os.path.join(vpn, "team{}".format(int(subnet))), filename="wg{}.conf".format(num),
                                   as_attachment=True)
    elif name == "ssh":
        return send_from_directory(ssh, filename="team{}".format(int(subnet)), as_attachment=True)
    else:
        return "error"


@app.route('/teams/', methods=['GET'])
def teams():
    events = Event.query.filter_by().order_by(Event.id.desc())
    return flask.render_template('teams.html', events=events)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        team = Team.query.filter_by(team_name=form.teamname.data).first()
        if team is not None:
            flash('Invalid teamname')
            return redirect(url_for('register'))

        t = Team()
        t.set_password(form.password.data)
        t.team_name = form.teamname.data
        db_session.add(t)
        db_session.commit()
        flash("Team is now registered. You can now log in")
        return flask.redirect(flask.url_for('login'))

    return flask.render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
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


@app.route("/validation_passwordreset/<team_id>/<hash>/")
def validation_passwordreset(team_id, hash):
    team = Team.query.filter_by(id=int(team_id)).first()

    if not team:
        flash("Team not found")

    else:
        if hash == team.password:
            members = Member.query.filter_by(team=team)
            users = [m.user for m in members]

            pw = generate_password(length=9)
            team.set_password(pw)
            db_session.commit()

            msg = Message(subject="Password Reset",
                          sender=config.MAIL_DEFAULT_SENDER,
                          reply_to=config.MAIL_REPLY_TO,
                          recipients=[u.email for u in users],
                          body="Password for your team was set to: {}".format(pw)
                          )
            mail.send(msg)

            flash('Email with new password was sent to all team members')
        else:
            flash("Incorrect Token")

    return flask.redirect(flask.url_for('index'))


@app.route('/passwordreset/', methods=['GET', 'POST'])
def passwordreset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        team = form.teamname.data
        team_id = team.id
        team = Team.query.filter_by(id=team_id).first()
        members = Member.query.filter_by(team=team)
        users = [m.user for m in members]

        msg = Message(subject="Password Reset",
                      sender=config.MAIL_DEFAULT_SENDER,
                      reply_to=config.MAIL_REPLY_TO,
                      recipients=[u.email for u in users],
                      body="Please validate your password reset request at {}{}".format(
                          config.URL_BASE,
                          url_for("validation_passwordreset", team_id=team.id, hash=team.password)),
                      )
        mail.send(msg)

        flash('Email was sent to all team members')

    return flask.render_template('passwordreset.html', form=form)


def first_empty_subnet():
    event = get_empty_event_or_fail()
    attending_teams = AttendingTeam.query.filter_by(event=event)
    used_nets = {a.subnet for a in attending_teams}
    free_nets = set(range(1, 250)).difference(used_nets)
    return list(free_nets)[0]


def get_empty_event_or_fail():
    event = Event.query.order_by(Event.id.desc()).first()
    if event is None:
        raise Exception("Cannot use a database without event.")
    if event.ticks.first():
        raise Exception("Cannot use an event with existing ticks. Create a new event.")
    return event


def send_validation_email(u, team):
    msg = Message(subject="Confirm your registration in CTF team",
                  sender=config.MAIL_DEFAULT_SENDER,
                  reply_to=config.MAIL_REPLY_TO,
                  recipients=[u.email],
                  body="You were added to the CTF team *{}*. To confirm your membership use this URL"
                       " {}{}".format(
                      team.team_name,
                      config.URL_BASE,
                      url_for("validation_user", token=u.token)),
                  )
    mail.send(msg)


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

        if datetime.now() > event.registration_end:
            flash("Registration time is over")
            return flask.redirect(flask.url_for('attend'))

        members_to_add = []

        def verify_member_form(tpl):
            if any(tpl):
                if not all(tpl):
                    return False
                return True
            return None

        def check_3_tuple(tpl):
            tpl = tuple(t.strip() for t in tpl)
            if verify_member_form(tpl) is False:
                flash("Fill all 3 fields for each member")
                return False
            # return flask.render_template('attend.html', form=form, members=team.members, attending=attending)
            elif verify_member_form(tpl) is True:
                if not tpl[0].endswith("@hs-albsig.de"):  # FIXME
                    flash("Please use only university email addresses")
                    return False
                # return flask.render_template('attend.html', form=form, members=team.members, attending=attending)
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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
