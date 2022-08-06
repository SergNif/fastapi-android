from database import Base, engine
# from models import Item
from fitmodels import User, Fitness

print("Creating database  ........")

Base.metadata.create_all(engine)