from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email

from db.database import db_session
from db.models import Team


class LoginForm(FlaskForm):
    teamname = StringField('Teamname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PasswordResetForm(FlaskForm):
    teamname = QuerySelectField(label='Teamname', query_factory=lambda: Team.query.filter_by(), get_pk=lambda x: x.id, get_label=lambda x: x, allow_blank=True)
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    teamname = StringField('Teamname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_teamname(self, username):
        team = Team.query.filter_by(team_name=username.data).first()
        if team is not None:
            raise ValidationError('Please use a different teamname.')

class AttendForm(FlaskForm):
    email1 = StringField('Email 1', validators=[])
    forename1 = StringField('Forename 1', validators=[])
    surname1 = StringField('Surname 1 ', validators=[])

    email2 = StringField('Email 2', validators=[])
    forename2 = StringField('Forename 2', validators=[])
    surname2 = StringField('Surname 2', validators=[])

    email3 = StringField('Email 3', validators=[])
    forename3 = StringField('Forename 3', validators=[])
    surname3 = StringField('Surname 3', validators=[])

    email4 = StringField('Email 4', validators=[])
    forename4 = StringField('Forename 4', validators=[])
    surname4 = StringField('Surname 4', validators=[])

    email5 = StringField('Email 5', validators=[])
    forename5 = StringField('Forename 5', validators=[])
    surname5 = StringField('Surname 5', validators=[])

    submit = SubmitField('Submit')


class UnregisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
