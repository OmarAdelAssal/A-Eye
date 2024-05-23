from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'gender', 'birthdate', 'date_joined')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('gender', 'date_joined')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': ('name', 'phone_number', 'gender', 'birthdate', 'address', 'image')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'phone_number', 'gender', 'birthdate', 'address', 'image')}
        ),
    )

admin.site.register(Customer, CustomerAdmin)
