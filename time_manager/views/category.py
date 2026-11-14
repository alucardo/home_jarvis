from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from time_manager.forms import CategoryForm
from time_manager.models import Category


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


@require_POST
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    category.delete()
    return redirect('time_manager:category_index')
