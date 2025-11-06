# shopapp/views.py
# Все представления, связанные с продуктами и заказами, размещаем здесь.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.core.cache import cache
from .models import Order, User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.syndication.views import Feed
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm, OrderForm
from django.utils.timezone import now
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from django.http import HttpResponse
import logging
logger = logging.getLogger('shopapp')

def example_view(request):
    logger.debug("Debug: Начало обработки запроса example_view")
    logger.info("Info: Запрос успешно обработан")
    logger.warning("Warning: Проверить потенциальную проблему")
    return HttpResponse("Пример работы логирования!")

# Главная страница магазина
def shop_index(request):
    products = Product.objects.filter(is_available=True)
    time_running = (now() - now().replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    context = {
        'products': products,
        'time_running': time_running,
    }
    return render(request, 'shopapp/shop-index.html', context)


# Sitemap для всех раздоступных товаров
class ShopSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_available=True)

    def location(self, item):
        return item.get_absolute_url()

# RSS-лента последних товаров
class LatestProductsFeed(Feed):
    title = "Новые товары магазина"
    link = "/products/latest/feed/"
    description = "Свежие товары в магазине"

    def items(self):
        return Product.objects.filter(is_available=True).order_by('-id')[:10]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()


# Список доступных продуктов
class ProductListView(ListView):
    model = Product
    template_name = 'shopapp/products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_available=True)



# Детальная страница продукта
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shopapp/product_detail.html'
    context_object_name = 'product'

# Создание нового продукта
class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'
    permission_required = 'shopapp.add_product'
    success_url = reverse_lazy('products_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

# Обновление товара
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'
    success_url = reverse_lazy('products_list')

    def test_func(self):
        user = self.request.user
        product = self.get_object()
        return user.is_superuser or (user.has_perm('shopapp.change_product') and product.created_by == user)

# Архивация продукта
class ProductArchiveView(View):
    template_name = 'shopapp/product_confirm_archive.html'

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, self.template_name, {'product': product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_available = True
        product.save()
        return redirect('products_list')

# Представления для заказа
# Список заказов
class OrderListView(ListView):
    model = Order
    template_name = 'shopapp/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.select_related('user').prefetch_related('products').all()

# Детали заказа
class OrderDetailView(DetailView):
    model = Order
    template_name = 'shopapp/order_detail.html'
    context_object_name = 'order'

# Создание заказа
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'shopapp/create_order.html'
    success_url = reverse_lazy('orders_list')

# Обновление заказа
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'shopapp/order_form.html'
    success_url = reverse_lazy('orders_list')

# Удаление заказа
class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'shopapp/order_confirm_delete.html'
    success_url = reverse_lazy('orders_list')

#ViewSet'ы для API:
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'quantity']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'user']
    ordering_fields = ['ordered_at', 'status']

#cache
class UserOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/user_orders_list.html'
    context_object_name = 'orders'

    def dispatch(self, request, *args, **kwargs):
        # Получаем пользователя по ID из URL или 404
        self.owner = get_object_or_404(User, pk=self.kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Возвращаем заказы пользователя сортируя по PK
        return Order.objects.filter(user=self.owner).order_by('pk').select_related('user').prefetch_related('products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner  # Чтобы в шаблоне был доступ к пользователю
        return context

class UserOrdersExportView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        cache_key = f'user_orders_export_{user.pk}'

        cached_data = cache.get(cache_key)
        if cached_data:
            return JsonResponse(cached_data, safe=False)

        orders = Order.objects.filter(user=user).order_by('pk').prefetch_related('products')
        serializer = OrderSerializer(orders, many=True)
        data = serializer.data

        cache.set(cache_key, data, timeout=300)  # Кеш 5 минут
        return JsonResponse(data, safe=False)