"""empty message

Revision ID: 1ea287df18aa
Revises: 
Create Date: 2020-05-28 10:57:18.186570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ea287df18aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clip',
    sa.Column('physical_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id', sa.BINARY(), nullable=False),
    sa.Column('text', sa.TEXT(), nullable=False),
    sa.Column('channel_name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('physical_id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clip')
    # ### end Alembic commands ###
