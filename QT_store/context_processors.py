from .models import *

def categories(request):
    categories = Category.objects.all()  # Получаем все категории из базы данных
    return {'categories': categories}  # Возвращаем словарь с категориями