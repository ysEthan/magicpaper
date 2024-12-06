from django.contrib import admin
from .models import Category, SPU, SKU

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name_zh', 'category_name_en', 'level', 'is_last_level', 
                   'status', 'rank_id', 'parent', 'get_full_path', 'created_at']
    list_filter = ['level', 'is_last_level', 'status']
    search_fields = ['id', 'category_name_zh', 'category_name_en', 'description']
    ordering = ['rank_id', 'id']
    raw_id_fields = ['parent']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('基本信息', {
            'fields': ('id', 'category_name_zh', 'category_name_en', 'description', 'image')
        }),
        ('分类结构', {
            'fields': ('parent', 'level', 'is_last_level', 'rank_id')
        }),
        ('其他信息', {
            'fields': ('original_data', 'status', 'created_at', 'updated_at')
        }),
    )

    def get_full_path(self, obj):
        return obj.get_full_path()
    get_full_path.short_description = '完整路径'


@admin.register(SPU)
class SPUAdmin(admin.ModelAdmin):
    list_display = ['id', 'spu_code', 'spu_name', 'sales_channel', 'category', 'created_at']
    list_filter = ['sales_channel', 'category']
    search_fields = ['id', 'spu_code', 'spu_name', 'spu_remark']
    ordering = ['-id']
    raw_id_fields = ['category']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 20

    fieldsets = (
        ('基本信息', {
            'fields': ('id', 'spu_code', 'spu_name', 'spu_remark')
        }),
        ('分类信息', {
            'fields': ('category', 'sales_channel')
        }),
        ('其他信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ['id', 'sku_code', 'sku_name', 'provider_name', 'unit_price', 
                   'plating_process', 'color', 'spu', 'created_at']
    list_filter = ['provider_name', 'plating_process', 'color', 'spu']
    search_fields = ['id', 'sku_code', 'sku_name', 'provider_name', 'plating_process', 'color']
    ordering = ['-id']
    raw_id_fields = ['spu']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 20

    fieldsets = (
        ('基本信息', {
            'fields': ('id', 'sku_code', 'sku_name', 'provider_name', 'spu')
        }),
        ('价格和重量', {
            'fields': ('unit_price', 'weight')
        }),
        ('规格信息', {
            'fields': ('plating_process', 'color', 'material', 'length', 'width', 'height', 'other_dimensions')
        }),
        ('图片信息', {
            'fields': ('img_url',)
        }),
        ('其他信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )
