from sqlalchemy import create_engine
from config import settings
from sqlalchemy.ext.declarative import declarative_base

ur_s = settings.POSTGRES_DATABASE_URLS
#ur_a = settings.POSTGRES_DATABASE_URLA



#engine = create_async_engine(ur_p, echo=True)
engine_s = create_engine(ur_s, echo=True)
Base = declarative_base(bind=engine_s)

#async def f():
  #  async with engine.begin() as conn:
       # answer = await conn.execute(text("select version()"))
      #  print(f"answer = {answer.all()}")

#asyncio.run(f())

def create_tables():
    Base.metadata.drop_all(bind=engine_s)
    Base.metadata.create_all(bind=engine_s)

#def f():
   #with engine_s.connect() as conn:
        #answer = conn.execute(text('select * from public."Employee";'))
       # print(f"answer = {answer.all()}")
