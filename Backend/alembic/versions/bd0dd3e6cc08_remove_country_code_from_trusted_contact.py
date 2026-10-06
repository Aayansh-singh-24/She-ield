"""remove country code from trusted contact

Revision ID: bd0dd3e6cc08
Revises: 8259cd593ed8
Create Date: 2026-10-06 12:16:29.240016

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bd0dd3e6cc08"
down_revision: Union[str, Sequence[str], None] = "8259cd593ed8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove country_code from trusted_contact
    op.drop_column(
        "trusted_contact",
        "country_code",
    )


def downgrade() -> None:
    # Restore country_code to trusted_contact
    op.add_column(
        "trusted_contact",
        sa.Column(
            "country_code",
            sa.VARCHAR(),
            nullable=True,
        ),
    )