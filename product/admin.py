from django.contrib import admin
from .models import Product, Category,District, Subdistrict,Subcategory
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
admin.site.register(Product)
admin.site.register(Category,CategoryAdmin)
admin.site.register(District,DistrictAdmin)
# admin.site.register(Subdistrict)
