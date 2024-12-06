from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from .models import Category, SPU
from .forms import CategoryForm, SPUForm

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
        # 检查是否有子类目
        children_count = category.children.count()
        if children_count > 0:
            messages.error(request, f'删除失败：该类目下还有{children_count}个子类目')
            return redirect('gallery:category_list')
        
        # 检查是否有关联的SPU
        spu_count = category.spus.count()
        if spu_count > 0:
            messages.error(request, f'删除失败：该类目下还有{spu_count}个关联的SPU')
            return redirect('gallery:category_list')
        
        category.delete()
        messages.success(request, '类目删除成功！')
    except ValidationError as e:
        messages.error(request, str(e))
    except ProtectedError:
        messages.error(request, '删除失败：该类目被其他数据引用')
    except Exception as e:
        messages.error(request, f'删除失败：{str(e)}')
    return redirect('gallery:category_list')

@login_required
def spu_list(request):
    """SPU列表页面"""
    spus = SPU.objects.all().select_related('category')
    return render(request, 'gallery/spu/list.html', {
        'spus': spus
    })

@login_required
def spu_add(request):
    """添加SPU页面"""
    if request.method == 'POST':
        form = SPUForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'SPU添加成功！')
            return redirect('gallery:spu_list')
    else:
        form = SPUForm()
    
    return render(request, 'gallery/spu/form.html', {
        'form': form,
        'title': '添加SPU',
        'submit_text': '添加'
    })

@login_required
def spu_update(request, pk):
    """修改SPU页面"""
    spu = get_object_or_404(SPU, pk=pk)
    if request.method == 'POST':
        # 从POST数据中排除spu_code字段
        post_data = request.POST.copy()
        post_data['spu_code'] = spu.spu_code  # 保持原有的spu_code值
        form = SPUForm(post_data, instance=spu)
        if form.is_valid():
            form.save()
            messages.success(request, 'SPU修改成功！')
            return redirect('gallery:spu_list')
    else:
        form = SPUForm(instance=spu)
    
    return render(request, 'gallery/spu/form.html', {
        'form': form,
        'title': '修改SPU',
        'submit_text': '保存'
    })

@login_required
def spu_delete(request, pk):
    """删除SPU"""
    spu = get_object_or_404(SPU, pk=pk)
    try:
        spu.delete()
        messages.success(request, 'SPU删除成功！')
    except Exception as e:
        messages.error(request, f'删除失败：{str(e)}')
    return redirect('gallery:spu_list')

