from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=(('available', 'Available'), ('unavailable', 'Unavailable')), default='available')
    category = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=10, blank=True, null=True)  # Optional field for size if needed
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'products'
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})
    
    def get_update_url(self):
        return reverse('product_update', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('product_delete', kwargs={'pk': self.pk})
    
    def get_search_url(self):
        return reverse('product_search')
    
    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'pk': self.pk})
    
    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'pk': self.pk})
    
    def get_checkout_url(self):
        return reverse('checkout')
    
    def get_order_history_url(self):
        return reverse('order_history')
    
    def get_order_detail_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True, null=True)  # Optional field for size if needed

    class Meta:
        unique_together = ('cart', 'product', 'size')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.quantity:
            self.quantity = 1

    def save(self, *args, **kwargs):
        # Ensure quantity is at least 1
        if self.quantity < 1:
            self.quantity = 1
        super().save(*args, **kwargs)

    def total_price(self):
        if self.product and self.quantity:
            return self.product.price * self.quantity
        return 0.0
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"