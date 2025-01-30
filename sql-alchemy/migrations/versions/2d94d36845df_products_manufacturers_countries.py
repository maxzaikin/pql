"""products, manufacturers, countries

Revision ID: 2d94d36845df
Revises: 
Create Date: 2025-01-30 23:29:54.016687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d94d36845df'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_countries'))
    )
    with op.batch_alter_table('countries', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_countries_name'), ['name'], unique=True)

    op.create_table('manufacturers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_manufacturers'))
    )
    with op.batch_alter_table('manufacturers', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_manufacturers_name'), ['name'], unique=True)

    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('manufacturer_id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('cpu', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['manufacturer_id'], ['manufacturers.id'], name=op.f('fk_products_manufacturer_id_manufacturers')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_products'))
    )
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_products_manufacturer_id'), ['manufacturer_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_products_name'), ['name'], unique=True)
        batch_op.create_index(batch_op.f('ix_products_year'), ['year'], unique=False)

    op.create_table('products_countries',
    sa.Column('prpduct_id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], name=op.f('fk_products_countries_country_id_countries')),
    sa.ForeignKeyConstraint(['prpduct_id'], ['products.id'], name=op.f('fk_products_countries_prpduct_id_products')),
    sa.PrimaryKeyConstraint('prpduct_id', 'country_id', name=op.f('pk_products_countries'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products_countries')
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_products_year'))
        batch_op.drop_index(batch_op.f('ix_products_name'))
        batch_op.drop_index(batch_op.f('ix_products_manufacturer_id'))

    op.drop_table('products')
    with op.batch_alter_table('manufacturers', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_manufacturers_name'))

    op.drop_table('manufacturers')
    with op.batch_alter_table('countries', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_countries_name'))

    op.drop_table('countries')
    # ### end Alembic commands ###
