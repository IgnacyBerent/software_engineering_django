FROM python:3.12
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/IgnacyBerent/software_engineering_django.git
WORKDIR /usr/src/app/software_engineering_django
RUN pip install -r requirements.txt
CMD ["python", "software_engineering/manage.py", "runserver", "0.0.0.0:9999"]