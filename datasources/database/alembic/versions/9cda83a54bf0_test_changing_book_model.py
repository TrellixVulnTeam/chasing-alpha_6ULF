"""test changing book model

Revision ID: 9cda83a54bf0
Revises: b250a14c4807
Create Date: 2022-04-07 22:21:43.070649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cda83a54bf0'
down_revision = 'b250a14c4807'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('coauthor', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'coauthor')
    # ### end Alembic commands ###