import datetime

from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import composite

from src.accounts.domain.models import Balance
from src.configs.database import Base


class Account(Base):
    __tablename__ = "accounts"

    account_number = Column(String, primary_key=True)
    owner_id = Column(String, ForeignKey("users.user_id"))
    account_password = Column(String, nullable=False)
    balance_amount = Column(Integer, nullable=False)

    balance = composite(Balance, balance_amount)


class TransactionEvent(Base):
    __tablename__ = "transaction_events"

    id = Column(Integer, primary_key=True)
    account_number = Column(String, ForeignKey("accounts.account_number"))
    transaction_datatime = Column(DateTime, default=datetime.datetime.utcnow)
    transaction_amount = Column(Integer)
    balance = Column(Integer)
    transaction_type = Column(String)
    memo = Column(String)
