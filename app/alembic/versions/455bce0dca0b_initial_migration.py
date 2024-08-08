"""Initial migration

Revision ID: 455bce0dca0b
Revises: 
Create Date: 2024-08-08 12:53:34.549188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '455bce0dca0b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_payments_id', table_name='payments')
    op.drop_table('payments')
    op.drop_index('ix_handymen_email', table_name='handymen')
    op.drop_index('ix_handymen_first_name', table_name='handymen')
    op.drop_index('ix_handymen_id', table_name='handymen')
    op.drop_index('ix_handymen_last_name', table_name='handymen')
    op.drop_index('ix_handymen_phone', table_name='handymen')
    op.drop_index('ix_handymen_username', table_name='handymen')
    op.drop_table('handymen')
    op.drop_index('ix_service_requests_id', table_name='service_requests')
    op.drop_table('service_requests')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_first_name', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_last_name', table_name='users')
    op.drop_index('ix_users_phone', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(), nullable=True),
    sa.Column('last_name', sa.VARCHAR(), nullable=True),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('phone', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=False)
    op.create_index('ix_users_phone', 'users', ['phone'], unique=1)
    op.create_index('ix_users_last_name', 'users', ['last_name'], unique=False)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_first_name', 'users', ['first_name'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=1)
    op.create_table('service_requests',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('handyman_id', sa.INTEGER(), nullable=True),
    sa.Column('car_make', sa.VARCHAR(), nullable=True),
    sa.Column('car_model', sa.VARCHAR(), nullable=True),
    sa.Column('car_year', sa.VARCHAR(), nullable=True),
    sa.Column('issue_description', sa.VARCHAR(), nullable=True),
    sa.Column('location', sa.VARCHAR(), nullable=True),
    sa.Column('status', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['handyman_id'], ['handymen.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_service_requests_id', 'service_requests', ['id'], unique=False)
    op.create_table('handymen',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(), nullable=True),
    sa.Column('last_name', sa.VARCHAR(), nullable=True),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('phone', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.Column('specialization', sa.VARCHAR(), nullable=True),
    sa.Column('rating', sa.FLOAT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_handymen_username', 'handymen', ['username'], unique=False)
    op.create_index('ix_handymen_phone', 'handymen', ['phone'], unique=1)
    op.create_index('ix_handymen_last_name', 'handymen', ['last_name'], unique=False)
    op.create_index('ix_handymen_id', 'handymen', ['id'], unique=False)
    op.create_index('ix_handymen_first_name', 'handymen', ['first_name'], unique=False)
    op.create_index('ix_handymen_email', 'handymen', ['email'], unique=1)
    op.create_table('payments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('service_request_id', sa.INTEGER(), nullable=True),
    sa.Column('amount', sa.FLOAT(), nullable=True),
    sa.Column('status', sa.VARCHAR(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['service_request_id'], ['service_requests.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_payments_id', 'payments', ['id'], unique=False)
    # ### end Alembic commands ###
