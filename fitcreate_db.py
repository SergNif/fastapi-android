from sqlmodel import SQLModel
from fitmodels import Userpage, Fitness, DataPage1, DataPage3, DataPage4, DataPage5, DataPage6, DataPage7, DataPage8, DataPage9, DataPage10, DataUser
from fitdatabase import engine

print("CREATING DATABASE.....")

SQLModel.metadata.create_all(engine)
