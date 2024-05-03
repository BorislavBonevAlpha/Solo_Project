from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from db_details import password, username, host
from typing import Annotated
from sqlalchemy.orm import Session

# to be continued


DATABASE_URL = f'mysql+pymysql://{username}:{password}@{host}/shift_seek'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


def insert_query(model, db, something):

    db_car = model(**something.dict())
    db.add(db_car)
    db.commit()

def read_query(model, db, param, property):

    result  = db.query(model).filter(getattr(model, property) == param).first()
    return result

def delete_query(user_model: User, db, something_id):

    db_record = db.query(user_model).filter(id=something_id).first()
    if db_record:
        db.delete(db_record)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail= 'This user was not found')
    