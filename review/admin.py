from django.contrib import admin
from .models import Review, ReviewMedia


class ReviewMediaInline(admin.TabularInline):
    model = ReviewMedia
    extra = 0  
    readonly_fields = ['media_type', 'file', 'uploaded_at']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at', 'get_media_count']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    readonly_fields = ['created_at', 'product', 'user', 'order', 'rating', 'comment']
    inlines = [ReviewMediaInline]
    
    def get_media_count(self, obj):
        """Hiển thị số lượng media files"""
        count = obj.media_files.count()
        if count > 0:
            images = obj.media_files.filter(media_type='image').count()
            videos = obj.media_files.filter(media_type='video').count()
            return f"{count} files ({images} ảnh, {videos} video)"
        return "Không có"
    get_media_count.short_description = 'Media'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False




# @admin.register(ReviewMedia)
# class ReviewMediaAdmin(admin.ModelAdmin):
#     list_display = ['review', 'media_type', 'get_thumbnail', 'uploaded_at']
#     list_filter = ['media_type', 'uploaded_at']
#     search_fields = ['review__product__name', 'review__user__username']
#     readonly_fields = ['review', 'media_type', 'file', 'uploaded_at', 'preview_media']
    
#     def get_thumbnail(self, obj):
#         """Hiển thị thumbnail trong list"""
#         if obj.media_type == 'image':
#             return f'<img src="{obj.file.url}" width="50" height="50" style="object-fit: cover;"/>'
#         else:
#             return '🎥 Video'
#     get_thumbnail.short_description = 'Preview'
#     get_thumbnail.allow_tags = True
    
#     def preview_media(self, obj):
#         """Hiển thị preview đầy đủ trong detail page"""
#         if obj.media_type == 'image':
#             return f'<img src="{obj.file.url}" style="max-width: 500px; max-height: 500px;"/>'
#         else:
#             return f'''
#                 <video controls style="max-width: 500px;">
#                     <source src="{obj.file.url}">
#                     Your browser does not support the video tag.
#                 </video>
#             '''
#     preview_media.short_description = 'Xem trước'
#     preview_media.allow_tags = True

#     def has_add_permission(self, request):
#         return False

#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False