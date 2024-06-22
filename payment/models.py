from django.db import models
from customers.models import Customer
from orders.models import Order

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('CC', 'Credit Card'),
        ('COD', 'Cash on Delivery'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE, default=1)  # Temporarily set a default order ID
    payment_method = models.CharField(max_length=3, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Set a default amount
    payment_date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id} by {self.customer.email}"