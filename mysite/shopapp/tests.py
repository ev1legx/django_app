from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from shopapp.models import Product, Order

class ShopAppTests(TestCase):
    def setUp(self):
        # Получаем content_type для модели Product и Order из приложения shopapp
        product_content_type = ContentType.objects.get(app_label='shopapp', model='product')
        order_content_type = ContentType.objects.get(app_label='shopapp', model='order')

        # Получаем необходимые разрешения по content_type
        permission_add_product = Permission.objects.get(codename='add_product', content_type=product_content_type)
        permission_change_product = Permission.objects.get(codename='change_product', content_type=product_content_type)
        permission_view_order = Permission.objects.get(codename='view_order', content_type=order_content_type)

        # Создаем пользователей
        # Пользователь с правами на добавление/изменение продуктов и просмотр заказов
        self.user_with_perm = User.objects.create_user(username='user1', password='pass')
        self.user_with_perm.user_permissions.add(permission_add_product, permission_change_product, permission_view_order)

        # Пользователь без специальных прав
        self.user_without_perm = User.objects.create_user(username='user2', password='pass')

        # Суперпользователь
        self.superuser = User.objects.create_superuser(username='admin', password='pass')

        # Создаем продукт для тестов
        self.product = Product.objects.create(
            name='Product1',
            description='Desc',
            price=10,
            quantity=5,
            is_available=True,
            created_by=self.user_with_perm
        )

        # Создаем заказ, связанный с пользователем с правами, добавляем продукт в заказ
        self.order = Order.objects.create(
            user=self.user_with_perm,
            status='new',
            comment='Initial order'  # если поле есть, иначе можно убрать
        )
        self.order.products.add(self.product)

        # Создаем тестовый клиент для имитации HTTP запросов
        self.client = Client()

    def test_product_list_view(self):
        # Проверяем, что страница списка продуктов доступна и содержит название продукта
        response = self.client.get(reverse('products_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_create_product_access(self):
        # Проверяем, что анонимный пользователь перенаправляется на страницу логина
        response = self.client.get(reverse('create_product'))
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('create_product'))

        # Проверяем, что пользователь без прав не может зайти на страницу создания продукта
        self.client.login(username='user2', password='pass')
        response = self.client.get(reverse('create_product'))
        self.assertTrue(response.status_code in [302, 403])
        self.client.logout()

        # Проверяем, что пользователь с правами имеет доступ к созданию продукта
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('create_product'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_edit_product_access(self):
        url = reverse('update_product', kwargs={'pk': self.product.pk})

        # Анонимный пользователь должен быть перенаправлен на логин
        response = self.client.get(url)
        self.assertRedirects(response, '/accounts/login/?next=' + url)

        # Пользователь без прав получает отказ
        self.client.login(username='user2', password='pass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # Пользователь с правами имеет доступ к редактированию продукта
        self.client.login(username='user1', password='pass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        # Суперпользователь тоже имеет доступ
        self.client.login(username='admin', password='pass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_order_list_view(self):
        # Пользователь с правами может просмотреть список заказов и видит имя пользователя
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('orders_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user_with_perm.username)
        self.client.logout()

    def test_order_detail_view(self):
        # Проверяем, что пользователь с правами может просмотреть детали заказа
        self.client.login(username='user1', password='pass')
        url = reverse('order_detail', kwargs={'pk': self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user_with_perm.username)
        self.client.logout()

    def test_product_str(self):
        # Проверка корректного строкового представления продукта
        self.assertEqual(str(self.product), 'Product1')

    def test_order_str(self):
        # Проверка корректного строкового представления заказа (начинается на "Order")
        self.assertTrue(str(self.order).startswith("Order"))
