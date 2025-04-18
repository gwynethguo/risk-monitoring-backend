"""Make client_id in positions not nullable

Revision ID: 589b7ccce624
Revises: f652cd54ca6d
Create Date: 2025-04-01 06:19:47.266032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '589b7ccce624'
down_revision: Union[str, None] = 'f652cd54ca6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('positions', 'client_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('positions', 'client_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
