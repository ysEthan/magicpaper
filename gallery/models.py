from django.db import models

class Category(models.Model):
    STATUS_CHOICES = (
        (1, '启用'),
        (0, '禁用'),
    )

    id = models.BigAutoField(primary_key=True, verbose_name='主键ID')
    category_name_en = models.CharField(max_length=100, verbose_name='英文名称')
    category_name_zh = models.CharField(max_length=100, verbose_name='中文名称')
    description = models.TextField(verbose_name='描述', blank=True, null=True)
    image = models.ImageField(upload_to='categories/', verbose_name='分类图片', blank=True, null=True)
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
