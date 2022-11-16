"""empty message

Revision ID: b95f5eed6330
Revises: 
Create Date: 2022-03-07 01:14:02.111766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b95f5eed6330'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'disttovendor', 'dist_vendor', ['vendor_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'disttovendor', type_='foreignkey')
    # ### end Alembic commands ###
