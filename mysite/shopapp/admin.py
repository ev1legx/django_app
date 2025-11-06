from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import csv
from .models import Product, Order
from .forms import UploadFileForm

class OrderInline(admin.TabularInline):
    model = Order.products.through
    extra = 1
    verbose_name = "Order"
    verbose_name_plural = "Orders"

def archive_products(modeladmin, request, queryset):
    queryset.update(is_available=False)
archive_products.short_description = "Archive selected products"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'quantity', 'is_available')
    search_fields = ('name', 'quantity')
    inlines = [OrderInline]
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Price Info', {'fields': ('price', 'quantity')}),
        ('Additional Options', {'fields': ('is_available',), 'classes': ('collapse',)}),
    )
    actions = [archive_products]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'ordered_at')
    search_fields = ('status', 'user__username')
    change_list_template = "admin/shopapp/order/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-orders/', self.admin_site.admin_view(self.import_orders_view), name='import_orders'),
        ]
        return my_urls + urls

    def import_orders_view(self, request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                try:
                    reader = csv.DictReader(file.read().decode('utf-8').splitlines())
                    for row in reader:
                        user_id = int(row['user_id'])
                        status = row['status']
                        product_ids = [int(pid) for pid in row['product_ids'].split(',')]
                        order = Order.objects.create(user_id=user_id, status=status)
                        order.products.add(*product_ids)
                    self.message_user(request, "Импорт успешно завершён", messages.SUCCESS)
                except Exception as e:
                    self.message_user(request, f"Ошибка импорта: {e}", messages.ERROR)
                return redirect('..')
        else:
            form = UploadFileForm()
        return render(request, "admin/csv_form.html", {'form': form})
