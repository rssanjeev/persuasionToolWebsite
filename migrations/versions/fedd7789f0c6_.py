"""empty message

Revision ID: fedd7789f0c6
Revises: 3fa4fa87005d
Create Date: 2018-09-05 15:26:31.166942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fedd7789f0c6'
down_revision = '3fa4fa87005d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Feedbacks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('textFeedback', sa.Text(), nullable=False),
    sa.Column('textInput', sa.Text(), nullable=False),
    sa.Column('persModels', sa.String(length=100), nullable=False),
    sa.Column('nonpersModels', sa.String(length=100), nullable=False),
    sa.Column('persuasive', sa.String(length=100), nullable=False),
    sa.Column('wordCount', sa.String(length=100), nullable=False),
    sa.Column('readabilityScore', sa.String(length=100), nullable=False),
    sa.Column('ReadabilityGrade', sa.String(length=100), nullable=False),
    sa.Column('DiractionCount', sa.String(length=100), nullable=False),
    sa.Column('WPS', sa.String(length=100), nullable=False),
    sa.Column('Sixltr', sa.String(length=100), nullable=False),
    sa.Column('pronoun', sa.String(length=100), nullable=False),
    sa.Column('ppron', sa.String(length=100), nullable=False),
    sa.Column('i', sa.String(length=100), nullable=False),
    sa.Column('you', sa.String(length=100), nullable=False),
    sa.Column('ipron', sa.String(length=100), nullable=False),
    sa.Column('prep', sa.String(length=100), nullable=False),
    sa.Column('auxverb', sa.String(length=100), nullable=False),
    sa.Column('negate', sa.String(length=100), nullable=False),
    sa.Column('numbers', sa.String(length=100), nullable=False),
    sa.Column('focuspast', sa.String(length=100), nullable=False),
    sa.Column('focuspresent', sa.String(length=100), nullable=False),
    sa.Column('AllPunc', sa.String(length=100), nullable=False),
    sa.Column('Comma', sa.String(length=100), nullable=False),
    sa.Column('QMark', sa.String(length=100), nullable=False),
    sa.Column('Exemplify', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Articles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Articles',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Articles_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Articles_pkey')
    )
    op.drop_table('Feedbacks')
    # ### end Alembic commands ###
