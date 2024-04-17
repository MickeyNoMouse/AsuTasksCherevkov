FROM python:3.11.0
RUN mkdir /fastapi_app
WORKDIR /fastapi_app
COPY requiremenets.txt .
RUN pip install -r requiremenets.txt
COPY . .
RUN python -c "import sqlalchemy; engine = sqlalchemy.create_engine('postgres://postgresuser:ZBDo4Vzb2m3fwFxDkvnvAG4k0QWPlBXG@dpg-coek0sol6cac73c6adq0-a.singapore-postgres.render.com/asutask3'); engine.connect()" || true
RUN alembic upgrade head
CMD gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
