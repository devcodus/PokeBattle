"""empty message

Revision ID: c66699ad6802
Revises: 9d1e64511c67
Create Date: 2023-01-22 16:21:37.103348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c66699ad6802'
down_revision = '9d1e64511c67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=45), nullable=False),
    sa.Column('ability_name', sa.String(length=45), nullable=False),
    sa.Column('base_xp', sa.Integer(), nullable=False),
    sa.Column('shiny', sa.String(length=200), nullable=False),
    sa.Column('attack', sa.Integer(), nullable=False),
    sa.Column('hp', sa.Integer(), nullable=False),
    sa.Column('defense', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemon')
    # ### end Alembic commands ###