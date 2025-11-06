from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product

class Command(BaseCommand):
    help = 'Create orders using get_or_create and link with existing products'

    def handle(self, *args, **kwargs):
        user = User.objects.first()  # например берем первого пользователя
        products = Product.objects.all()

        order_data = {
            'comment': 'Order comment example',
            'status': 'new',
            'user': user
        }

        order, created = Order.objects.get_or_create(
            comment=order_data['comment'],
            status=order_data['status'],
            user=user
        )
        if created:
            order.products.set(products)  # связываем с продуктами
            order.save()
        action = "Created" if created else "Existing"
        self.stdout.write(f"{action} order with id: {order.id}")
