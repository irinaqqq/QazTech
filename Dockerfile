# Используем официальный образ Python в качестве базового  
FROM python:3.13-slim  
  
# Устанавливаем рабочую директорию  
WORKDIR /app  
  
# Устанавливаем системные зависимости  
RUN apt-get update \  
    && apt-get install -y build-essential libpq-dev gcc \  
    && rm -rf /var/lib/apt/lists/*  
  
# Копируем файлы проекта  
COPY . /app  
  
# Устанавливаем зависимости проекта  
RUN pip install --no-cache-dir -r requirements.txt  
  
# Открываем порт, который будет использоваться вашим приложением  
EXPOSE 8000  
  
# Копируем и устанавливаем права на скрипт  
COPY entrypoint.sh /entrypoint.sh  
RUN chmod +x /entrypoint.sh  
  
# Используем скрипт в качестве точки входа  
CMD ["/entrypoint.sh"]  