from django.shortcuts import render
from category.models import Category

# Create your views here.
def home(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }
    return render(request, 'user_template/home.html', context)


