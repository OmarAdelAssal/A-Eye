from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from customers.models import Customer
from products.models import Product
from django.utils import timezone
# Create your models here.
@receiver(post_save, sender=Customer)
def create_cart_for_customer(sender, instance, created, **kwargs):
    """
    Signal handler to create a cart for a user profile when it is created.
    """
    if created:
        # Create a cart for the user profile
        Cart.objects.create(customer=instance)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.customer)+' '+'cart'
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Default to 1 when a new cart item is created

    class Meta:
        unique_together = ['cart', 'product']  # Ensure each product is added to the cart only once
    
    def __str__(self):
        return f"Owner: {self.cart.customer.name}, Product: {self.product.name}"