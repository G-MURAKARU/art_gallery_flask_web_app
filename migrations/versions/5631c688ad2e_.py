"""empty message

Revision ID: 5631c688ad2e
Revises: 13163bc5929a
Create Date: 2019-05-11 09:19:44.493398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5631c688ad2e'
down_revision = '13163bc5929a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artistPreferences',
    sa.Column('customerName', sa.String(length=120), nullable=True),
    sa.Column('artistName', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['artistName'], ['artists.artistName'], ),
    sa.ForeignKeyConstraint(['customerName'], ['customers.customerName'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artistPreferences')
    # ### end Alembic commands ###