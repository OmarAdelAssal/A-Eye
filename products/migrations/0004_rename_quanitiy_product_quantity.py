# Generated by Django 4.2.7 on 2024-05-22 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='quanitiy',
            new_name='quantity',
        ),
    ]
