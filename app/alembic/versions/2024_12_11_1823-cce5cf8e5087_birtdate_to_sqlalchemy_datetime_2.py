"""birtdate to sqlalchemy.DateTime 2

Revision ID: cce5cf8e5087
Revises: ea80233c0d61
Create Date: 2024-12-11 18:23:14.943044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cce5cf8e5087'
down_revision: Union[str, None] = 'ea80233c0d61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
