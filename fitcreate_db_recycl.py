from sqlmodel import SQLModel
from fitmodels_recycl import RecyclPage
from fitdatabase_recycl import engine

print("CREATING DATABASE.....")

SQLModel.metadata.create_all(engine)
