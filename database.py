from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Finding database Url
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

#create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False})

# create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declare mapping
Base = declarative_base()



