from .models import *

def categories(request):
    categories = Category.objects.all().order_by('id')  
    return {'categories': categories}