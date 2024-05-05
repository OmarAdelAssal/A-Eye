from django.db import models

# Create your models here.

# Class for Categories like chairs , Tables ,etc ....
class Category(models.Model):
    categoryName = models.CharField(max_length=200,null=True ,blank=True)

    def __str__(self):
        return self.categoryName


class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    quanitiy = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',default=0)

    def __str__(self):
        return self.name


