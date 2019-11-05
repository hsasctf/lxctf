"""empty message

Revision ID: a4272eaee700
Revises: 
Create Date: 2019-04-27 12:36:14.861770

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a4272eaee700'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team_files')
    op.alter_column('team', 'is_admin',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('team', 'is_admin',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    op.create_table('team_files',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('attending_team_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('created', mysql.DATETIME(), nullable=True),
    sa.Column('updated', mysql.DATETIME(), nullable=True),
    sa.Column('ovpn', sa.BLOB(), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=9), nullable=False),
    sa.Column('ssh', sa.BLOB(), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
