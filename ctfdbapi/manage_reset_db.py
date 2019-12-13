import sys
from db.database import db_session


from db.models import AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, Tick, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun, \
    TeamScore, TeamServiceState

if not input("delete all content of db?") == "yes":
    sys.exit(0)

[model.query.delete() for model in [
    TeamScore, AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, Tick,
    TeamServiceState, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun
]]
db_session.commit()
print("done")
