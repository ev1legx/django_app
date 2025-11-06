
# Маршруты магазина — продукты и заказы.
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet
from . import views

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', views.shop_index, name='shop_index'),

    # Продукты
    path('products/', views.ProductListView.as_view(), name='products_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', views.ProductCreateView.as_view(), name='create_product'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:pk>/archive/', views.ProductArchiveView.as_view(), name='archive_product'),

    # Заказы
    path('orders/', views.OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/create/', views.OrderCreateView.as_view(), name='create_order'),
    path('order/<int:pk>/update/', views.OrderUpdateView.as_view(), name='update_order'),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='delete_order'),

    # Подключение маршрутов DRF через include
    path('api/', include(router.urls)),
]

from .views import UserOrdersListView, UserOrdersExportView

urlpatterns += [
    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_orders_list'),
    path('users/<int:user_id>/orders/export/', UserOrdersExportView.as_view(), name='user_orders_export'),
]
