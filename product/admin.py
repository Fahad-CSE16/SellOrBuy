from django.contrib import admin
from .models import Product, Category,District, Subdistrict,Subcategory,Order, OrderItem
from django.contrib.admin import ModelAdmin
from django.utils import timezone
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','address','status','paid','created_at')
    list_filter = ('user', )
    actions = ('set_status_shipped','set_status_arrived')
    search_fields = ( 'user__username',)
    list_display_links = ('user', 'address',)
    # filter_horizontal= ('subject','class_in','preferedPlace','views','likes')
    # list_select_related=('district',)
    list_editable = ('status',)
    inlines = [
        OrderItemInline,
    ]
    def set_status_shipped(self, request, queryset):
        count = queryset.update(status='Shipped')
        self.message_user(request, '{} posts updated'.format(count))
    set_status_shipped.short_description='Set Shipped'
    def set_status_arrived(self, request, queryset):
        count = queryset.update(status='Arrived')
        self.message_user(request, '{} posts updated'.format(count))
    set_status_arrived.short_description='Set Arrived'
    # def get_subjects(self, obj):
    #     return ", ".join([p.name for p in obj.subject.all()])
    # get_subjects.short_description = 'Subjects'
    
# Register your models here.
class SubDistrictInline(admin.TabularInline):
    model = Subdistrict

class DistrictAdmin(admin.ModelAdmin):
    inlines = [
        SubDistrictInline,
    ]
class SubCategoryInline(admin.TabularInline):
    model = Subcategory

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubCategoryInline,
    ]
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user','name','available_quantity')
admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Category,CategoryAdmin)
admin.site.register(District,DistrictAdmin)
# admin.site.register(Subdistrict)
