# Generated by Django 5.1.7 on 2025-04-03 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_cartitem_size'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product', 'size')},
        ),
    ]
