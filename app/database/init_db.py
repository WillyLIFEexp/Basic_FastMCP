from app.database.session import engine
from app.database.base_class import Base
from app.models.user import User

def init_db():
    Base.metadata.create_all(bind=engine)