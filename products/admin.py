from django.contrib import admin

# Register your models here.

from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName','categoryLogo',)
    search_fields = ('categoryName',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    raw_id_fields = ('category',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)