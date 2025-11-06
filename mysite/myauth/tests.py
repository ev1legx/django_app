from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthViewsTest(TestCase):

    def test_signup_page_loads(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_creates_user(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123'
        })
        self.assertRedirects(response, reverse('shop_index'))
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logout_redirect(self):
        user = User.objects.create_user(username='admin', password='adminpassword')
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
