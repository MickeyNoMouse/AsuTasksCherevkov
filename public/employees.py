from fastapi import APIRouter, Body, Path, Query, Response, Depends
from models.model import Main_Employee, Main_EmployeeDB, New_Respons, Employee, Base
from typing import Annotated
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from config import settings
from fastapi.exceptions import HTTPException
from db import engine_s



#engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#def init_db():
    #Base.metadata.create_all(bind=engine)

def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()

employees_router = APIRouter(prefix = "/employees", tags=["Сотрудники"])

def coder_passwd(cod: str):
    return cod*2

#employees_list = [Main_EmployeeDB(name='Ivanov', id=103, password ='*****', age = 35, post = "manager"),
                 # Main_EmployeeDB(name='Petrov', id=129, password ='*******', age = 20, post = "student")]

def find_employee(id: int) -> Main_EmployeeDB | None:
    for employee in employees_list:
        if employee.id == id:
            return employee
    return None

@employees_router.get("/show", response_model= list[Main_EmployeeDB] | New_Respons)
def get_employees(DB: Session = Depends(get_session)):
    employees = DB.query(Employee).all()
    if employees == []:
        return New_Respons(message='Пользователи не найдены')
    return employees

#@employees_router.get("/showQuery", response_model= Main_Employee | New_Respons)
#def get_users(id: Annotated[int, Query(..., gt = 0)]):
  #  employee = find_employee(id)
   # print(employee)
    #if employee == None:
     #   return New_Respons(message='Пользователь не найден')
    #return employee

@employees_router.get("/show/{id}", response_model= Main_EmployeeDB | New_Respons)
def get_employee(id: Annotated[int, Path(..., gt = 0)], DB: Session = Depends(get_session)):
    employee = DB.query(Employee).filter(Employee.id == id).first()
    #employee = find_employee(id)
    print(employee)
    if employee == None:
        return New_Respons(message='Пользователь не найден')
    return employee

@employees_router.post("/create", response_model= Main_Employee | New_Respons)
def create_employee(item: Annotated[Main_Employee, Body(embed=True, description="New User")],
                    DB: Session = Depends(get_session)):
    try:
        employee = Employee(id=item.id, name=item.name, age=item.age, post=item.post, hashed_password=coder_passwd(item.name))
        if employee is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(employee)
        DB.commit()
        DB.refresh(employee)
        return employee
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении объекта {employee}")

@employees_router.put("/update/{id}", response_model= Main_Employee | New_Respons)
def edit_employee(item: Annotated[Main_Employee, Body(embed=True, description="Обновление данных User'a по id")],
                  id: Annotated[int, Path(..., gt = 0)], DB: Session = Depends(get_session)):
    #employee = find_employee(id)
    employee = DB.query(Employee).filter(Employee.id == item.id).first()
    if employee == None:
        return New_Respons(message='Пользователь не найден')
    employee.name = item.name
    employee.age = item.age
    employee.post = item.post
    try:
        DB.commit()
        DB.refresh(employee)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return employee

@employees_router.delete("/delete/{id}", response_model= New_Respons)
def delete_employee(id: Annotated[int, Path(..., gt = 0)], DB: Session = Depends(get_session)):
    employee = DB.query(Employee).filter(Employee.id == id).first()
    if employee is None:
       return New_Respons(message='Пользователь не найден')
    try:
       DB.delete(employee)
       DB.commit()
    except HTTPException:
       JSONResponse(content={'message' : f'Ошибка'})
    return New_Respons(message='Пользователь  удалён')



@employees_router.patch("/update/{id}", response_model= Main_Employee | New_Respons)
def edit_employee(post: str=Query(None,embed=True) , name: str=Query(None,embed=True), age: int=Query(None,embed=True),
                  id: int = Path(..., gt=0), DB: Session = Depends(get_session)):
    employee = DB.query(Employee).filter(Employee.id == id).first()
    if employee == None:
        return New_Respons(message='Пользователь не найден')
    if post is not None:
        employee.post = post
    if name is not None:
        employee.name = name
    if age is not None:
        employee.age = age
    try:
        DB.commit()
        DB.refresh(employee)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": ""})
    return employee