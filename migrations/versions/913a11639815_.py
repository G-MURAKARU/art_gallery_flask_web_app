"""empty message

Revision ID: 913a11639815
Revises: f311e01059eb
Create Date: 2019-05-10 10:00:16.043878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '913a11639815'
down_revision = 'f311e01059eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'groupings_ibfk_2', 'groupings', type_='foreignkey')
    op.drop_constraint(u'groupings_ibfk_1', 'groupings', type_='foreignkey')
    op.create_foreign_key(None, 'groupings', 'groups', ['groupName'], ['groupName'], onupdate='cascade')
    op.create_foreign_key(None, 'groupings', 'artwork', ['title'], ['title'], onupdate='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'groupings', type_='foreignkey')
    op.drop_constraint(None, 'groupings', type_='foreignkey')
    op.create_foreign_key(u'groupings_ibfk_1', 'groupings', 'groups', ['groupName'], ['groupName'])
    op.create_foreign_key(u'groupings_ibfk_2', 'groupings', 'artwork', ['title'], ['title'])
    # ### end Alembic commands ###
