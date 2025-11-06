from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        # Возвращает ссылку на детальную страницу товара
        return reverse('product_detail', args=[str(self.pk)])

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

class Order(models.Model):
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=50)
    ordered_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
