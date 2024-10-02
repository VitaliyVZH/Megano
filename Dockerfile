FROM python:3.7

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==1.7.1"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY megano .

CMD ["gunicorn", "megano.wsgi:application", "--bind", "0.0.0.0:8000"]