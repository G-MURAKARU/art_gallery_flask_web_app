"""empty message

Revision ID: 9200400516ac
Revises: 65750f6f02d3
Create Date: 2019-05-15 09:39:52.645992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9200400516ac'
down_revision = '65750f6f02d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artStyles',
    sa.Column('artistName', sa.String(length=120), nullable=True),
    sa.Column('styleName', sa.String(length=40), nullable=True),
    sa.ForeignKeyConstraint(['artistName'], ['artists.artistName'], onupdate='cascade'),
    sa.ForeignKeyConstraint(['styleName'], ['styles.styleName'], onupdate='cascade')
    )
    op.create_table('groupings',
    sa.Column('title', sa.String(length=120), nullable=True),
    sa.Column('groupName', sa.String(length=60), nullable=True),
    sa.ForeignKeyConstraint(['groupName'], ['groups.groupName'], onupdate='cascade'),
    sa.ForeignKeyConstraint(['title'], ['artwork.title'], onupdate='cascade')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('groupings')
    op.drop_table('artStyles')
    # ### end Alembic commands ###
