from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product
User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    @property
    def total_price(self):
        return sum([item.total_subprice for item in self.items.objects.all()])

    def __str__(self):
        return self.user.email

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)


    class Meta:
        unique_together = ['cart', 'product']

    @property
    def total_subprice(self):
        return self.quantity * self.product.price
    
