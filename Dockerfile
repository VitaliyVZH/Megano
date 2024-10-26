# Используйте базовый образ Python с поддержкой пользователя
FROM python:3.10-slim-buster

# Установите переменную окружения для отключения буферизации вывода Python
ENV PYTHONUNBUFFERED=1

# Установите рабочую директорию на /app
WORKDIR /app

# Установите переменную окружения для Django
ENV DJANGO_SETTINGS_MODULE=megano.settings

# Обновите список пакетов и установите Nginx
RUN apt-get update && apt-get install -y nginx

# Создайте пользователя nginx
RUN useradd -r -u 101 -g www-data -M nginx

# Копируем файл конфигурации Gunicorn в рабочую директорию
COPY ./gunicorn.conf.py /app/gunicorn.conf.py

# Устанавливаем poetry
RUN pip install "poetry==1.8.2"

# Настраиваем poetry, чтобы оно не создавало виртуальное окружение
RUN poetry config virtualenvs.create false --local

# Копируем файлы и директории проекта в рабочую директорию
COPY megano/ /app/megano/
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости проекта с помощью poetry
RUN poetry install

# Укажите команду для запуска контейнера: сначала запустите Nginx в фоновом режиме, затем запустите Gunicorn с конфигурацией из файла gunicorn.conf.py и приложением megano.wsgi:application
RUN pip install gevent
CMD ["nginx", "-g", "daemon off;", "&&", "gunicorn", "-c", "/app/gunicorn.conf.py", "--chdir", "/app", "--workers=3", "--bind=unix:/run/gunicorn.sock", "--user=nginx", "megano.wsgi:application"]