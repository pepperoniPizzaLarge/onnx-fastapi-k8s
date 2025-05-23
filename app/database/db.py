import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# SQL_DATABASE_URL = "sqlite:///./onnxFastapi.db"

# engine = create_engine(SQL_DATABASE_URL, connect_args={'check_same_thread': False})

engine = create_engine(
    "postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}".format(
        db_username=os.environ['PGUSER'], 
        db_password=os.environ['PGPASSWORD'],
        db_host=os.environ['PGHOST'],
        db_port=os.environ['PGPORT'],
        db_name=os.environ['PGDATABASE']
        )
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
