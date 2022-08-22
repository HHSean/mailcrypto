###############################################################################
# Database
#
# This module is used to interact with the PostgreSQL database (hosted on Render)
###############################################################################

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, MetaData
from sqlalchemy.orm import sessionmaker
import json
import csv
import datetime
import os


from dotenv import load_dotenv
load_dotenv("../.env")

DB_URI = os.getenv("DB_URI").replace("postgres://", "postgresql://")

meta = MetaData()

# store: sender, recipient, key, amount, message, created_at, updated_at
deposits = Table(
    "deposits",
    meta,
    Column("id", Integer, primary_key=True),
    Column("sender", String),
    Column("recipient", String),
    Column("key", String),
    Column("amount", Integer),
    Column("message", String),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("accepted", Boolean),
)

engine = create_engine(DB_URI, echo=False)
meta.create_all(engine)
Session = sessionmaker(bind=engine)



def insert_deposit(sender, recipient, key, amount, message):

    session = Session()
    deposit = deposits.insert().values(
        sender=sender,
        recipient=recipient,
        key=key,
        amount=amount,
        message=message,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
        accepted=False,
    )
    session.execute(deposit)
    session.commit()
    return


def get_deposit(key):
    session = Session()
    deposit = session.query(deposits).filter(deposits.c.key == key).first()
    return deposit


def update_deposit(key, accepted):
    session = Session()
    deposit = session.query(deposits).filter(deposits.c.key == key).first()
    deposit.accepted = accepted
    deposit.updated_at = datetime.datetime.now()
    session.commit()
    return deposit


def get_all_deposits():
    session = Session()
    return session.query(deposits).all()


def download_deposits():
    session = Session()
    table = session.query(deposits).all()
    # store to csv
    with open("deposits.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "sender", "recipient", "key", "amount", "message", "created_at", "updated_at", "accepted"])
        for deposit in table:
            writer.writerow([deposit.id, deposit.sender, deposit.recipient, deposit.key, deposit.amount, deposit.message, deposit.created_at, deposit.updated_at, deposit.accepted])


# util functions

def print_all_tables():
    # prints the name of all tables in the database
    session = Session()
    for table in session.get_bind().engine.table_names():
        print(table)

def reset_deposits():
    # deletes the contents of the deposits table
    session = Session()
    session.query(deposits).delete()
    session.commit()
    return

    
if __name__ == "__main__":
    # insert test deposit
    sender = "0x1234567890123456789012345678901234567890"
    recipient = "hello@world.com"
    key = "1234567890123456789012345678901234567890"
    amount = 1
    message = "test"
    deposit = insert_deposit(sender, recipient, key, amount, message)
    print(deposit)

    # get test deposit
    deposit = get_deposit(key)
    print(deposit)


    # download all deposits
    # download_deposits()
    
    print_all_tables()
    
