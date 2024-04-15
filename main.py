from fastapi import FastAPI
from public.employees import employees_router #, init_db
#from db import create_tables
import pytest

#from db import create_tables

app = FastAPI()

#create_tables()

app.include_router(employees_router)

#@app.on_event("startup")
#def on_startup():
    #open("log.txt", mode="a").write(f'{datetime.utcnow()}: Begin\n')
    #init_db()

#@app.on_event("shutdown")
#def shutdown():
    #open("log.txt", mode="a").write(f'{datetime.utcnow()}: End\n')



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
