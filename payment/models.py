# Create your models here.
from django.db import models
from django.utils import timezone
from customers.models import Customer


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = (
        ('Credit Card', 'Credit Card'),
        ('Cash on Delivery ', 'Cash on Delivery'),

    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment {self.id} - {self.customer.name}"
