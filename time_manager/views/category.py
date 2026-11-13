from django.shortcuts import render

def category_index(request):
    categories = request.user.time_categories.all()
    return render(request, 'time_manager/category/index.html', {'categories': categories})
