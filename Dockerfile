FROM python:3.9
LABEL maintainer="django-pokemon-api"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app/app
EXPOSE 8000

RUN pip install -r /tmp/requirements.txt && rm -rf /tmp/requirements.txt

RUN python3 manage.py migrate

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
