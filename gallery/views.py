from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
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

@login_required
def category_update(request, pk):
    """修改类目页面"""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, '类目修改成功！')
            return redirect('gallery:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'gallery/category/form.html', {
        'form': form,
        'title': '修改类目',
        'submit_text': '保存'
    })

@login_required
def category_delete(request, pk):
    """删除类目"""
    category = get_object_or_404(Category, pk=pk)
    try:
        category.delete()
        messages.success(request, '类目删除成功！')
    except Exception as e:
        messages.error(request, f'删除失败：{str(e)}')
    return redirect('gallery:category_list')

