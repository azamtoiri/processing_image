"""update status to state

Revision ID: 0004
Revises: 0003
Create Date: 2024-06-30 15:01:55.004836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0004'
down_revision: Union[str, None] = '0003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('state', sa.String(length=50), nullable=False, default='uploaded'))
    op.drop_column('images', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False, default='uploaded'))
    op.drop_column('images', 'state')
    # ### end Alembic commands ###