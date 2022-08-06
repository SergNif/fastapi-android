from sqlalchemy import table
from sqlmodel import Relationship, SQLModel, Field
from typing import Optional, List
from sqlalchemy import UniqueConstraint, Column, String
from datetime import datetime



class RecyclPage(SQLModel, table=True):
    # __tablename__='pageuser'
    id_tab:Optional[int] = Field(default=None, primary_key = True)
    id: int
    date : str # = "" #Column(Date, nullable = False)#": "May 4, 2022 12:20:55 PM",
    age : int #Column(Integer, nullable= False)#": 30,
    date : str #Column(Date, nullable = False)#": "May 4, 2022 12:19:31 PM",
    time : str #Column(Date, nullable = False)#": "May 4, 2022 12:19:31 PM",
    desired_weight: float #Column(Float(10, 2))#": 50.0,
    height : int #Column(Integer, nullable= False)#": 20,
    weight : float #Column(Float(10, 2))#": 40.0
    header: str
    menu: str
    
