"""rename phone number to email

Revision ID: 8259cd593ed8
Revises:
Create Date: 2026-10-06 11:23:35.748901

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "8259cd593ed8"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename phoneNo column to email
    op.alter_column(
        "trusted_contact",
        "phoneNo",
        new_column_name="email",
    )

    # Remove old phone number index
    op.drop_index(
        "ix_trusted_contact_phoneNo",
        table_name="trusted_contact",
    )

    # Create new email index
    op.create_index(
        "ix_trusted_contact_email",
        "trusted_contact",
        ["email"],
        unique=False,
    )


def downgrade() -> None:
    # Rename email back to phoneNo
    op.alter_column(
        "trusted_contact",
        "email",
        new_column_name="phoneNo",
    )

    # Remove email index
    op.drop_index(
        "ix_trusted_contact_email",
        table_name="trusted_contact",
    )

    # Recreate phone number index
    op.create_index(
        "ix_trusted_contact_phoneNo",
        "trusted_contact",
        ["phoneNo"],
        unique=False,
    )