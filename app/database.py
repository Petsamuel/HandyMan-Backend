from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from databases import Database
import os
from dotenv import load_dotenv
load_dotenv();



# DATABASE_URL = os.getenv("POSTGRES_URL")
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
# POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
# POSTGRES_URL_NO_SSL = os.getenv("POSTGRES_URL_NO_SSL")
# DB_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{5432}/{POSTGRES_DATABASE}"

database = Database(POSTGRES_URL)
metadata = MetaData()
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



