from django.contrib import admin
from .models import Category

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
