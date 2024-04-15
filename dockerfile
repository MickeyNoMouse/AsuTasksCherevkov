FROM python:3.11.0
RUN mkdir /fastapi_app
WORKDIR /fastapi_app
COPY requiremenets.txt .
RUN pip install -r requiremenets.txt
COPY . .
RUN alembic upgrade head
CMD gunicorn main:app --workers 2 --worker-class вuvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
