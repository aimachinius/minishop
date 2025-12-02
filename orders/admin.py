from django.contrib import admin
from .models import Order, OrderItem
# from django.shortcuts import redirect
# from django.urls import reverse

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    def has_add_permission(self, request, obj):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'city', 'status', 'created_at', 'get_total_cost']
    list_filter = ['status', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['status']
    
    def get_total_cost(self, obj):
        return f"{obj.get_total_cost():,.0f} VND"
    get_total_cost.short_description = 'Tổng tiền'

    def has_add_permission(self, request):
        return False
    def get_readonly_fields(self, request, obj=None):
        """
        Khi edit, tất cả các field ngoài 'status' sẽ readonly
        """
        if obj:  # đang edit
            return [f.name for f in self.model._meta.fields if f.name != 'status']
        return []  # khi tạo mới, tất cả editable
    def has_delete_permission(self, request, obj=None):
        return False
