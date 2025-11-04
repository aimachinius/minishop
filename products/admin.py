from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product
from review.models import Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['created_at']


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0 # khong cho admin tao form moi de them review 
    readonly_fields = ['user', 'rating', 'comment', 'created_at']
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created_at', 'image_tag']
    list_filter = ['available', 'created_at', 'updated_at', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    inlines = [ReviewInline]
    
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "Không có hình"
    image_tag.short_description = 'Hình ảnh'
    def has_delete_permission(self, request, obj = ...):
        return super().has_delete_permission(request, obj)


