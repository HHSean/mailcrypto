###############################################################################
# Database
#
# This module is used to interact with the PostgreSQL database (hosted on Render)
###############################################################################

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, MetaData, Float
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
    # l = request.form["email"]
    #         amount = request.form["amount"]
    #         message = request.form["message"]
    #         tx_hash = request.form["txHash"]
    #         deposit_index = request.form["depositIndex"]
    Column("id", Integer, primary_key=True),
    Column("key", String),
    Column("deposit_index", Integer),
    Column("sender", String),
    Column("recipient", String),
    Column("tx_hash", String),
    Column("amount", Float),
    Column("message", String),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("accepted", Boolean),
)

engine = create_engine(DB_URI, echo=False)
meta.create_all(engine)
Session = sessionmaker(bind=engine)



def insert_deposit(sender, recipient, key, amount, message, tx_hash, deposit_index):

    amount = float(amount)
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
        tx_hash=tx_hash,
        deposit_index=deposit_index,
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

def check_key(key):
    # checks if a key is in the database
    session = Session()
    deposit = session.query(deposits).filter(deposits.c.key == key).first()
    if deposit is None:
        return False
    else:
        return True


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
    # drop table deposits
    meta.drop_all(engine)
    # create table deposits
    meta.create_all(engine)


