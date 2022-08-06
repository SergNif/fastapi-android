from lib2to3.pytree import Base
from click import echo
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# engine = create_engine("postgresql://fastapi:123@localhost/item_db", echo = True,  connect_args={"check_same_thread": False} )
engine = create_engine("postgresql://fitnes:123@localhost/fitness_w_db", echo = True,  connect_args={"check_same_thread": False} )

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)
Base = declarative_base()
