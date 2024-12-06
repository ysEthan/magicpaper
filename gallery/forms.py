from django import forms
from .models import Category, SPU

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name_zh', 'category_name_en', 'description', 'image',
                 'parent', 'rank_id', 'level', 'is_last_level', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 获取所有可用的父类目
        self.fields['parent'].queryset = Category.objects.filter(
            is_last_level=False,
            status=1
        ).order_by('rank_id')


class SPUForm(forms.ModelForm):
    class Meta:
        model = SPU
        fields = ['spu_code', 'spu_name', 'spu_remark', 'sales_channel', 'category']
        widgets = {
            'spu_remark': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'spu_code': forms.TextInput(attrs={'class': 'form-control'}),
            'spu_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sales_channel': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 获取所有可用的类目
        self.fields['category'].queryset = Category.objects.filter(
            status=1
        ).order_by('rank_id')
        
        # 如果是编辑模式（实例已存在），则SPU编码不可修改
        if self.instance and self.instance.pk:
            self.fields['spu_code'].widget.attrs['readonly'] = True
            self.fields['spu_code'].widget.attrs['class'] = 'form-control bg-light'