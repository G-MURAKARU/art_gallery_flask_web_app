"""empty message

Revision ID: 65750f6f02d3
Revises: e6d1ef7a431f
Create Date: 2019-05-11 21:06:21.206868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65750f6f02d3'
down_revision = 'e6d1ef7a431f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'artistpreferences_ibfk_1', 'artistPreferences', type_='foreignkey')
    op.drop_constraint(u'artistpreferences_ibfk_2', 'artistPreferences', type_='foreignkey')
    op.create_foreign_key(None, 'artistPreferences', 'customers', ['customerName'], ['customerName'], onupdate='cascade')
    op.create_foreign_key(None, 'artistPreferences', 'artists', ['artistName'], ['artistName'], onupdate='cascade')
    op.drop_constraint(u'grouppreferences_ibfk_2', 'groupPreferences', type_='foreignkey')
    op.drop_constraint(u'grouppreferences_ibfk_1', 'groupPreferences', type_='foreignkey')
    op.create_foreign_key(None, 'groupPreferences', 'customers', ['customerName'], ['customerName'], onupdate='cascade')
    op.create_foreign_key(None, 'groupPreferences', 'groups', ['groupName'], ['groupName'], onupdate='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'groupPreferences', type_='foreignkey')
    op.drop_constraint(None, 'groupPreferences', type_='foreignkey')
    op.create_foreign_key(u'grouppreferences_ibfk_1', 'groupPreferences', 'customers', ['customerName'], ['customerName'])
    op.create_foreign_key(u'grouppreferences_ibfk_2', 'groupPreferences', 'groups', ['groupName'], ['groupName'])
    op.drop_constraint(None, 'artistPreferences', type_='foreignkey')
    op.drop_constraint(None, 'artistPreferences', type_='foreignkey')
    op.create_foreign_key(u'artistpreferences_ibfk_2', 'artistPreferences', 'customers', ['customerName'], ['customerName'])
    op.create_foreign_key(u'artistpreferences_ibfk_1', 'artistPreferences', 'artists', ['artistName'], ['artistName'])
    # ### end Alembic commands ###
