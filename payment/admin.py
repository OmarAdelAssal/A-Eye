from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'payment_method', 'payment_date')
    search_fields = ('customer__name', 'payment_method')
    list_filter = ('payment_method', 'payment_date')
    ordering = ('-payment_date',)

admin.site.register(Payment, PaymentAdmin)
