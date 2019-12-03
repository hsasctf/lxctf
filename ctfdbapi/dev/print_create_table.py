from sqlalchemy.sql.ddl import CreateTable

import db
from db.database import db_session, engine
from db.models import TeamScore, AttendingTeam, Event, Team, Submission, Flag, Challenge, Sla, Member, User, Tick, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun, \
    TeamServiceState

if __name__ == "__main__":



    for model in [TeamScore, AttendingTeam, Event, Team, Submission, Flag, Challenge, Sla, Member, User, Tick, TeamServiceState, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun]:
        print(CreateTable(model.__table__).compile(engine))
