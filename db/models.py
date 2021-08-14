from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

from db.base import Base


users_currencies = Table(
    'users_currencies',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('currency_id', Integer, ForeignKey('currencies.id', ondelete='CASCADE'))
)


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    short_title = Column(String(length=32))
    title = Column(String(length=64), unique=True, nullable=False)
    rate = Column(Float)
    users = relationship(
        'User', secondary='users_currencies', back_populates='currencies', passive_deletes=True
    )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    telegram_id = Column(Integer, nullable=False, unique=True)
    currencies = relationship(
        'Currency', secondary='users_currencies', back_populates='users', passive_deletes=True
    )
