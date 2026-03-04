from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv('SQL_URL')
# DATABASE_URL = "mysql+pymysql://root:Man29%402005@localhost:3306/db1"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()