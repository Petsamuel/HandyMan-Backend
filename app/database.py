from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from databases import Database
import os
from dotenv import load_dotenv
load_dotenv();

# Determine the environment
ENV = os.getenv("ENV", "development")  # Default to development if not set

# Set up database URL based on the environment
if ENV == "production":
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
    PORT =5432
    
    DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{PORT}/{POSTGRES_DATABASE}"
else:
    # Use SQLite for local development
    DB_URL ="postgresql://postgres:root@localhost:5432/handyman"
#    DATABASE_URL=postgresql://postgres:root@localhost:5432/handyman
#            postgresql://username:password@localhost:5432/dbname
    # DB_URL ="sqlite:///./handyman.db"

database = Database(DB_URL)

metadata = MetaData()

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



