from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated
from sqlalchemy import Column, String, Integer, Identity
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Employee(Base):
    __tablename__ = "Employee"
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, Identity(start = 1), primary_key=True)
    name = Column(String, index=True, nullable=False)
    age = Column(Integer)
    post = Column(String)
    hashed_password = Column(String)


class Main_Employee(BaseModel):
    name : Annotated [str | None, Field(min_length=2)] = "DefaultUser"
    id : Annotated[int | None, Field(default=100, ge=1, lt = 200)]
    age : Annotated[int | None, Field(ge=18)]
    post : Annotated[str | None, Field(min_length=3)] = "NonePost"

class Main_EmployeeDB(Main_Employee):
    hashed_password: Annotated[str | None, Field(max_length = 200, min_length = 5)] = None

class New_Respons(BaseModel):
    message : Annotated[str, Field(min_length=5)] = "Какая-то ошибка"
