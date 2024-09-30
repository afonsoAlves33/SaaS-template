from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = 'sqlite:///sqlite_database.db'

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():

    try:
        session = Session()
        yield session
    finally:
        session.close()


if __name__ == "__main__":
    from app.db.models import Base
    Base.metadata.create_all(bind=engine)

