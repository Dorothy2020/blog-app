from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Finding database Url
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

#create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declare mapping
Base = declarative_base()

def get_db():
    db = SessionLocal()  # this from database
    try:
        yield db
    finally:
        db.close()  # everything is done close the db


