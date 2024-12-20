from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.decorators import log_errors
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@log_errors
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()