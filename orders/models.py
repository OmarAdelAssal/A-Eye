from django.db import models
from django.utils import timezone
from customers.models import Customer
from products.models import Product

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    order_date = models.DateTimeField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Order, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'Order {self.order_id} by {self.customer}'

    class Meta:
        ordering = ['-created_at']