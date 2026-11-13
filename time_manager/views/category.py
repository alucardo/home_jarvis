from django.shortcuts import render, redirect

from time_manager.forms import CategoryForm


def category_index(request):
    categories = request.user.time_categories.all()
    return render(request, 'time_manager/category/index.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('time_manager:category_index')
    else:
        form = CategoryForm(user=request.user)

    return render(request, 'time_manager/category/create.html', {'form': form})