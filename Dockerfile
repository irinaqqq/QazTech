# Используем официальный образ Python в качестве базового  
FROM python:3.13-slim  
  
# Устанавливаем рабочую директорию  
WORKDIR /app  
  
# Копируем файлы проекта  
COPY . /app  
  
# Устанавливаем зависимости проекта  
RUN pip install --no-cache-dir -r requirements.txt  
  
# Открываем порт, который будет использоваться вашим приложением  
EXPOSE 8000  
  
# Команда для выполнения миграций и запуска приложения  
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]  