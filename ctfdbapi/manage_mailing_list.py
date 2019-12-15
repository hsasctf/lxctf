"""
Helper script for printing email addresses of all attending users
"""

from app_register import get_empty_event_or_fail
from db.database import db_session
from db.models import AttendingTeam


def emaillist():
   event = get_empty_event_or_fail()
   attending_teams = AttendingTeam.query.filter_by(event=event)
   teams = [a.team for a in attending_teams]
   members = [t.members for t in teams]
   emails = [m2.user.email for m in members for m2 in m]

   return ' '.join(emails)

if __name__ == '__main__':
    print(emaillist())