#!/bin/sh  
  
# Выполнение миграций  
python manage.py migrate  
  
# Запуск сервера  
python manage.py runserver 0.0.0.0:8000  