"""empty message

Revision ID: bd0a18b13134
Revises: 
Create Date: 2022-06-16 10:26:19.842310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd0a18b13134'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Table Users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('namec', sa.String(length=255), nullable=True),
    sa.Column('correo', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo')
    )
    op.create_table('flights',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('departureDate', sa.DateTime(), nullable=True),
    sa.Column('departureAirportCode', sa.String(length=60), nullable=True),
    sa.Column('departureAirportName', sa.String(length=100), nullable=True),
    sa.Column('departureCity', sa.String(length=255), nullable=True),
    sa.Column('departureLocale', sa.String(length=255), nullable=True),
    sa.Column('arrivalDate', sa.DateTime(), nullable=True),
    sa.Column('arrivalAirportCode', sa.String(length=60), nullable=True),
    sa.Column('arrivalAirportName', sa.String(length=100), nullable=True),
    sa.Column('arrivalCity', sa.String(length=255), nullable=True),
    sa.Column('arrivalLocale', sa.String(length=255), nullable=True),
    sa.Column('ticketPrice', sa.Integer(), nullable=True),
    sa.Column('ticketCurrency', sa.String(length=60), nullable=True),
    sa.Column('flightNumber', sa.Integer(), nullable=True),
    sa.Column('seatCapacity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Bookings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.String(length=40), nullable=True),
    sa.Column('outboundFlight_id', sa.Integer(), nullable=True),
    sa.Column('paymentToken', sa.String(length=100), nullable=True),
    sa.Column('checkedIn', sa.Boolean(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('bookingReference', sa.String(length=40), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['Table Users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['outboundFlight_id'], ['flights.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bookingReference')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Bookings')
    op.drop_table('flights')
    op.drop_table('Table Users')
    # ### end Alembic commands ###