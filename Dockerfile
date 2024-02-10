FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/payhere_test/payhere_project

WORKDIR /app/payhere_test/payhere_project
COPY ./payhere_test/payhere_project/* ./
# upgrade pip #botocore 
RUN pip install --upgrade pip
RUN pip install --upgrade python-dateutil
RUN pip install -r requirements.txt

COPY . /app/

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]