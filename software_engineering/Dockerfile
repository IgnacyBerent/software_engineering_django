FROM python:3.12
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY requirements.txt .
WORKDIR /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 9999
CMD ["python", "software_engineering/manage.py", "runserver", "0.0.0.0:9999"]