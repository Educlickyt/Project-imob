from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
# from app.core.config import settings

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@database:5432/realestate"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

