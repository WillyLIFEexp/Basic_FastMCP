from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    pool_size=5,              # Number of connections to keep in the pool
    max_overflow=10,          # Number of extra connections allowed above pool_size
    pool_timeout=30,          # Seconds to wait before giving up on getting a connection
    pool_recycle=1800         # Seconds after which a connection is recycled
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()