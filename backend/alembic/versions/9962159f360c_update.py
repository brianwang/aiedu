"""update

Revision ID: 9962159f360c
Revises: 42e8ce0e3c96
Create Date: 2025-05-29 11:59:31.520719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9962159f360c'
down_revision: Union[str, None] = '42e8ce0e3c96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite不支持直接添加外键约束，跳过外键约束创建
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # SQLite不支持直接删除外键约束，跳过外键约束删除
    pass
