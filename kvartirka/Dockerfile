# pull official base image
FROM python:3.8

RUN apt-get update && apt-get install -y netcat

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# install dependencies
RUN mkdir /app

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml /app 
COPY poetry.lock /app
RUN poetry install --no-dev

# copy project
COPY . .

# run entrypoint
RUN ["chmod", "+x", "/app/entrypoint.sh"]
ENTRYPOINT ["/app/entrypoint.sh"]
# RUN python3 manage.py collectstatic --noinput
# CMD python3 manage.py runserver 0:8000 