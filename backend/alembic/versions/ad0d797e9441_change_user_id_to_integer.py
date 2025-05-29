"""change user id to integer

Revision ID: ad0d797e9441
Revises: e81e5a28b8da
Create Date: 2025-05-29 10:35:30.724716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ad0d797e9441'
down_revision: Union[str, None] = 'e81e5a28b8da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('id',
                              existing_type=sa.VARCHAR(),
                              type_=sa.Integer(),
                              existing_nullable=False,
                              autoincrement=True)


def downgrade() -> None:
    """Downgrade schema."""
    pass
