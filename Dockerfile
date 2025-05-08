FROM python:3.13-slim

# Создание рабочей директории
WORKDIR /app

# Копирование зависимостей и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт для gunicorn
EXPOSE 8000

# Запуск через gunicorn — лучше для продакшена
CMD ["gunicorn", "QT_website.wsgi:application", "--bind", "0.0.0.0:8000"]