import datetime
import random
import string
import enum

from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, TEXT

from sqlalchemy.dialects.mysql import LONGBLOB

from sqlalchemy import DECIMAL
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint, create_engine
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.ddl import CreateTable

from config import SQLALCHEMY_DATABASE_URI
from hash_passwort import generate_password
from .database import Base

from hashlib import sha512

POSSIBILITIES = string.ascii_uppercase + string.digits + string.ascii_lowercase


class ModelBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.now)
    updated = Column(DateTime, default=datetime.datetime.now,
                     onupdate=datetime.datetime.now)


class AttendingTeam(ModelBase):
    __tablename__ = "attending_team"

    __table_args__ = (
        UniqueConstraint('event_id', 'team_id', name='attendingteams_uc_event_team'),
        UniqueConstraint('event_id', 'subnet', name='attendingteams_uc_event_subnet'),
    )

    event_id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    event = relationship('Event',
                         backref=backref('participants', cascade="all, delete-orphan", lazy='dynamic'))

    team_id = Column(Integer, ForeignKey('team.id', ondelete='CASCADE'), nullable=False)
    team = relationship('Team',
                        backref=backref('participations', cascade="all, delete-orphan", lazy='dynamic'))
    subnet = Column(Integer, nullable=False, unique=False)

    def __str__(self):
        return "AttendingTeam ID: {} (Event:{}) {} - Subnet {}".format(self.id, self.event, self.team, self.subnet)


class Event(ModelBase):
    __tablename__ = "event"

    # FIXME mysql igngores this
    __table_args__ = (
        CheckConstraint('registration_start < registration_end', name='event_check_regstart_lt_regend'),
        CheckConstraint('registration_end < start', name='event_check_regstart_lt_start'),
        CheckConstraint('start < attack_defense_start', name='event_check_start_lt_adstart'),
        CheckConstraint('attack_defense_start < end', name='event_check_adstart_lt_end'),
    )
    registration_start = Column(DateTime)
    registration_end = Column(DateTime)
    start = Column(DateTime)
    attack_defense_start = Column(DateTime)
    end = Column(DateTime)
    is_demo = Column(TINYINT(display_width=1), default=0)

    def __str__(self):
        return "Event {} - Start {}".format(self.id, self.start)


class Team(ModelBase, UserMixin):
    __tablename__ = "team"

    team_name = Column(String(64), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    password_salt = Column(String(128), nullable=False)
    last_login = Column(DateTime, default=None, nullable=True)
    is_admin = Column(TINYINT(display_width=1), default=None, nullable=True)

    def set_password(self, password):
        salt = ''.join(random.choice(POSSIBILITIES) for x in range(128))
        self.password_salt = salt
        self.password = sha512("{}{}".format(password, salt).encode("utf8")).hexdigest()

    def check_password(self, password):
        return self.password == sha512("{}{}".format(password, self.password_salt).encode("utf8")).hexdigest()

    def __str__(self):
        return "{}".format(self.team_name)  # used for password reset! do not change

class User(ModelBase):
    __tablename__ = "user"
    
    forename = Column(String(35), nullable=False)
    surname = Column(String(35), nullable=False)
    email = Column(String(254), nullable=False)
    token = Column(String(128), nullable=True)
    verified = Column(DateTime, default=None, nullable=True)

    def __str__(self):
        return "User: Name {}, {} - Email {}".format(self.surname, self.forename, self.email)

    def ensure_token(self):
        if not self.token or len(self.token) < 10:
            self.token = generate_password(64)


class Member(ModelBase):
    __tablename__ = "member"

    team_id = Column(Integer, ForeignKey('team.id', ondelete='CASCADE'))
    team = relationship('Team',
                        backref=backref('members', cascade="all, delete-orphan", lazy='dynamic'))

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship('User',
                        backref=backref('members', cascade="all, delete-orphan", lazy='dynamic'))

    # TODO unique together

    def __str__(self):
        return "Member: {} (Team: {})".format(self.user, self.team)


class ChallengeTypes(enum.Enum):
    jeopardy = 0
    ad = 1


class Challenge(ModelBase):
    __tablename__ = "challenge"

    event_id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    event = relationship('Event',
                         backref=backref('challenges', cascade="all, delete-orphan", lazy='dynamic'))

    name = Column(String(64), unique=True, nullable=False)
    description = Column(TEXT, nullable=False)
    points = Column(Integer, nullable=False, default=100)

    port = Column(Integer, nullable=True)
    type = Column(Enum(ChallengeTypes), nullable=False)
    jeopardy_flag = Column(String(128), nullable=True)  # must be NULL/None if AD

    authors = Column(String(2048), nullable=True)

    flag_id_description = Column(String(2048), nullable=True)

    def __str__(self):
        return "Challenge ID {}: {} ({}), Type: {}".format(self.id, self.name, self.points, self.type)


class Submission(ModelBase):
    __tablename__ = "submission"
    attending_team_id = Column(Integer, ForeignKey('attending_team.id', ondelete='CASCADE'), nullable=False)
    attending_team = relationship('AttendingTeam',
                                  backref=backref('submissions', cascade="all, delete-orphan", lazy='dynamic'))

    # flag_id is not Flag.flag_id......
    flag_id = Column(Integer, ForeignKey('flag.id', ondelete='CASCADE'), default=None, nullable=True, unique=False)
    flag = relationship('Flag',
                        backref=backref('submissions', cascade="all, delete-orphan", lazy='dynamic'))

    # TODO should be None/NULL when no matching flag could be found
    submitted_string = Column(String(128), nullable=False)

    def __str__(self):
        return "Submission by {}, String: {}, Flag: {}".format(self.attending_team, self.submitted_string, self.flag)


class Flag(ModelBase):
    __tablename__ = "flag"

    # __table_args__ = (
    #     CheckConstraint('static_jeopardy_flag or attending_team_id not null', name='check_static_flag'),
    # )

    # defending team
    attending_team_id = Column(Integer, ForeignKey('attending_team.id', ondelete='CASCADE'), nullable=False)
    attending_team = relationship('AttendingTeam',
                                  backref=backref('flags', cascade="all, delete-orphan", lazy='dynamic'))

    challenge_id = Column(Integer, ForeignKey('challenge.id', ondelete='CASCADE'), nullable=False)
    challenge = relationship('Challenge',
                             backref=backref('flags', cascade="all, delete-orphan", lazy='dynamic'))

    flag = Column(String(128), nullable=False)

    # cookie and flag_id are nullable because scorebot sets them after creating a new flag
    cookie = Column(String(5000), nullable=True)
    flag_id = Column(String(5000), nullable=True)

    # static_jeopardy_flag = Column(Boolean, default=False) # TODO WEG DAMIT

    def __str__(self):
        return "Flag of {}".format(self.attending_team)


class Tick(ModelBase):
    __tablename__ = "tick"

    # created, id
    # ...
    time_to_change = Column(DateTime, nullable=False)

    event_id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    event = relationship('Event',
                         backref=backref('ticks', cascade="all, delete-orphan", lazy='dynamic'))

    def __str__(self):
        return "Tick: ID: {}, Created: {}".format(self.id, self.created)


class ScriptType(enum.Enum):
    getflag = 1
    setflag = 2
    benign = 3
    exploit = 4


class Script(ModelBase):
    __tablename__ = "script"

    type = Column(Enum(ScriptType), nullable=False)

    event_id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    event = relationship('Event',
                         backref=backref('scripts', cascade="all, delete-orphan", lazy='dynamic'))

    challenge_id = Column(Integer, ForeignKey('challenge.id', ondelete='CASCADE'), nullable=False)
    challenge = relationship('Challenge',
                             backref=backref('scripts', cascade="all, delete-orphan", lazy='dynamic'))

    is_working = Column(TINYINT(display_width=1), default=1, nullable=True)
    is_bundle = Column(TINYINT(display_width=1), default=0, nullable=False)
    name = Column(String(64), nullable=False)

    # feedback = Column(String(500), nullable=False)

    def __str__(self):
        return "Script: {} {}".format(self.challenge, self.name)


class ScriptPayload(ModelBase):
    __tablename__ = "script_payload"

    script_id = Column(Integer, ForeignKey('script.id', ondelete='CASCADE'), nullable=False)
    script = relationship('Script',
                          backref=backref('script_payloads', cascade="all, delete-orphan", lazy='dynamic'))

    payload = Column(LONGBLOB, nullable=False)


class TeamScriptsRunStatus(ModelBase):
    """
    list of scripts to run on a team created by gamebot
    """

    __tablename__ = "team_scripts_run_status"

    attending_team_id = Column(Integer, ForeignKey('attending_team.id', ondelete='CASCADE'), nullable=False)
    attending_team = relationship('AttendingTeam',
                                  backref=backref('team_script_run_status', cascade="all, delete-orphan",
                                                  lazy='dynamic'))

    json_list_of_scripts_to_run = Column(TEXT, nullable=False)

    tick_id = Column(Integer, ForeignKey('tick.id', ondelete='CASCADE'), nullable=False)
    tick = relationship('Tick',
                        backref=backref('team_script_run_status', cascade="all, delete-orphan", lazy='dynamic'))


class ScriptRun(ModelBase):
    """
    send by REST API when scorebots runs a script
    when there was no exception:
    error_msg is "Init"
    error is 0

    Other Error codes
    ERROR_SCRIPT_EXECUTION = (0xA003,"Script execution failed.")
ERROR_WRONG_FLAG = (0x1000, "Error wrong flag.")
ERROR_DB = (0x9000,"DB error.")
ERROR_SCRIPT_KILLED = (0xB000,"Script was killed by the scheduler.")
    """

    __tablename__ = "script_run"

    # defending team:
    attending_team_id = Column(Integer, ForeignKey('attending_team.id', ondelete='CASCADE'), nullable=False)
    attending_team = relationship('AttendingTeam',
                                  backref=backref('script_runs', cascade="all, delete-orphan", lazy='dynamic'))

    error = Column(Integer, nullable=False)

    error_msg = Column(String(2048), nullable=True)

    script_id = Column(Integer, ForeignKey('script.id', ondelete='CASCADE'), nullable=False)
    script = relationship('Script',
                          backref=backref('script_runs', cascade="all, delete-orphan", lazy='dynamic'))


class TeamServiceState(ModelBase):
    __tablename__ = "team_service_state"

    attending_team_id = Column(Integer, ForeignKey('attending_team.id', ondelete='CASCADE'), nullable=False)
    attending_team = relationship('AttendingTeam',
                                  backref=backref('team_service_states', cascade="all, delete-orphan", lazy='dynamic'))

    challenge_id = Column(Integer, ForeignKey('challenge.id', ondelete='CASCADE'), nullable=False)
    challenge = relationship('Challenge',
                             backref=backref('team_service_states', cascade="all, delete-orphan", lazy='dynamic'))

    state = Column(Integer, nullable=False)
    reason = Column(String(256), nullable=False)

    def __str__(self):
        return "({} -> {} -> {},{})".format(self.attending_team, self.challenge, self.state, self.reason)


class TeamScore(ModelBase):
    __tablename__ = "team_score"

    attending_team_id = Column(Integer, ForeignKey('attending_team.id', ondelete='CASCADE'), nullable=False)
    attending_team = relationship('AttendingTeam',
                                  backref=backref('team_scores', cascade="all, delete-orphan", lazy='dynamic'))

    score = Column(Integer, nullable=False)
    reason = Column(String(256), nullable=False)
