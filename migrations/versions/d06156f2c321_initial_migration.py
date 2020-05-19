"""initial migration

Revision ID: d06156f2c321
Revises: 
Create Date: 2020-05-18 15:05:05.275964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd06156f2c321'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Expenditure',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ExpenditureCategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('expenditure_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['Category.id'], ),
    sa.ForeignKeyConstraint(['expenditure_id'], ['Expenditure.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ExpenditureCategory')
    op.drop_table('Expenditure')
    op.drop_table('Category')
    # ### end Alembic commands ###