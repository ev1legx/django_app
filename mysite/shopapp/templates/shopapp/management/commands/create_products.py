from django.core.management.base import BaseCommand
from shopapp.models import Product

class Command(BaseCommand):
    help = 'Create products using get_or_create'

    def handle(self, *args, **kwargs):
        products_data = [
            {'name': 'Product 1', 'description': 'Description 1', 'price': 10.00, 'quantity': 20, 'is_available': True},
            {'name': 'Product 2', 'description': 'Description 2', 'price': 15.50, 'quantity': 30, 'is_available': True},
        ]
        for data in products_data:
            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'price': data['price'],
                    'quantity': data['quantity'],
                    'is_available': data['is_available'],
                }
            )
            action = "Created" if created else "Existing"
            self.stdout.write(f"{action} product: {product.name}")
