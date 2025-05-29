"""empty message

Revision ID: cea9c4581776
Revises: fbad37812747
Create Date: 2025-05-29 10:31:27.920362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cea9c4581776'
down_revision: Union[str, None] = 'fbad37812747'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
