from django.db import models
from django.db.models import ProtectedError
from django.core.exceptions import ValidationError

class Category(models.Model):
    STATUS_CHOICES = (
        (1, '启用'),
        (0, '禁用'),
    )

    id = models.BigAutoField(primary_key=True, verbose_name='主键ID')
    category_name_en = models.CharField(max_length=100, verbose_name='英文名称')
    category_name_zh = models.CharField(max_length=100, verbose_name='中文名称')
    description = models.TextField(verbose_name='描述', blank=True, null=True)
    image = models.ImageField(upload_to='images', verbose_name='分类图片', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='父类目', 
                             related_name='children', blank=True, null=True)
    rank_id = models.IntegerField(verbose_name='排序ID', default=0)
    original_data = models.CharField(max_length=255, verbose_name='原始数据', blank=True, null=True)
    level = models.IntegerField(verbose_name='层级', default=1)
    is_last_level = models.BooleanField(verbose_name='是否是最后一级', default=False)
    status = models.IntegerField(verbose_name='状态', choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '类目'
        verbose_name_plural = '类目'
        ordering = ['rank_id', 'id']
        db_table = 'gallery_category'

    def __str__(self):
        return f"{self.category_name_zh} ({self.category_name_en})"

    def get_full_path(self):
        """获取完整的类目路径"""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.category_name_zh}"
        return self.category_name_zh

    def delete(self, *args, **kwargs):
        """重写删除方法，添加删除前检查"""
        # 检查是否有子类目
        if self.children.exists():
            raise ValidationError('无法删除：该类目下还有子类目')
        
        # 检查是否有关联的SPU
        if self.spus.exists():
            raise ValidationError('无法删除：该类目下还有关联的SPU')
            
        super().delete(*args, **kwargs)


class SPU(models.Model):
    SALES_CHANNEL_CHOICES = (
        (1, '线上商城'),
        (2, '线下门店'),
        (3, '电商平台'),
        (4, '批发渠道'),
        (5, '其他渠道'),
    )

    id = models.BigAutoField(primary_key=True, verbose_name='主键ID')
    spu_code = models.CharField(max_length=50, unique=True, verbose_name='SPU编码')
    spu_name = models.CharField(max_length=200, verbose_name='SPU名称')
    spu_remark = models.TextField(verbose_name='SPU备注', blank=True, null=True)
    sales_channel = models.IntegerField(
        verbose_name='销售渠道',
        choices=SALES_CHANNEL_CHOICES,
        default=1
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='所属类目',
        related_name='spus'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = 'SPU'
        verbose_name_plural = 'SPU'
        ordering = ['-id']
        db_table = 'gallery_spu'

    def __str__(self):
        return f"{self.spu_code} - {self.spu_name}"


class SKU(models.Model):
    COLOR_CHOICES = (
        ('gold', '金色'),
        ('silver', '银色'),
        ('rose_gold', '玫瑰金'),
        ('black', '黑色'),
        ('white', '白色'),
        ('blue', '蓝色'),
        ('red', '红色'),
        ('green', '绿色'),
        ('purple', '紫色'),
        ('yellow', '黄色'),
        ('other', '其他'),
    )

    id = models.BigAutoField(primary_key=True, verbose_name='主键ID')
    sku_code = models.CharField(max_length=50, unique=True, verbose_name='SKU编码')
    sku_name = models.CharField(max_length=200, verbose_name='SKU名称')
    provider_name = models.CharField(max_length=100, verbose_name='供应商名称')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    weight = models.PositiveIntegerField(verbose_name='重量(g)')
    plating_process = models.CharField(max_length=100, verbose_name='电镀工艺')
    color = models.CharField(
        max_length=20, 
        choices=COLOR_CHOICES,
        verbose_name='颜色'
    )
    length = models.PositiveIntegerField(verbose_name='长度(mm)')
    width = models.PositiveIntegerField(verbose_name='宽度(mm)')
    height = models.PositiveIntegerField(verbose_name='高度(mm)')
    other_dimensions = models.CharField(max_length=50, verbose_name='其他尺寸', blank=True, null=True)
    img_url = models.ImageField(upload_to='images', verbose_name='SKU图片', blank=True, null=True)
    material = models.CharField(max_length=100, verbose_name='材质')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    spu = models.ForeignKey(
        SPU,
        on_delete=models.CASCADE,
        verbose_name='所属SPU',
        related_name='skus'
    )

    class Meta:
        verbose_name = 'SKU'
        verbose_name_plural = 'SKU'
        ordering = ['-id']
        db_table = 'gallery_sku'

    def __str__(self):
        return f"{self.sku_code} - {self.sku_name}"
