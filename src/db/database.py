import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

USER  = os.environ.get("POSTGRES_USER", "db_admin")
PASSWORD  = os.environ.get("POSTGRES_PASSWORD", "db_admin")
DB  = os.environ.get("POSTGRES_DB", "hasty")

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@postgresserver/{DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
