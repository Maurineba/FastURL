FROM python:3.12-slim


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY . /code


CMD ["sh", "-c", "alembic upgrade head && fastapi dev app/main.py --port 8000 --host 0.0.0.0"]
