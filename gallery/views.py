from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category
from .forms import CategoryForm

@login_required
def category_list(request):
    """类目列表页面"""
    categories = Category.objects.all().order_by('rank_id', 'id')
    return render(request, 'gallery/category/list.html', {
        'categories': categories
    })

@login_required
def category_add(request):
    """添加类目页面"""
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '类目添加成功！')
            return redirect('gallery:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'gallery/category/form.html', {
        'form': form,
        'title': '添加类目',
        'submit_text': '添加'
    })

