from django import forms
from django.forms import ModelForm
from .models import Product, Order
from django.core.exceptions import ValidationError


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Выберите файл')

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'is_available']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['comment', 'status', 'user', 'products']

    # Проверка отдельного поля, например, status
    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in ['new', 'processing', 'completed']:
            raise ValidationError('Недопустимый статус заказа')
        return status

    # Общая проверка формы (поля вместе, например, условие на comment)
    def clean(self):
        cleaned_data = super().clean()
        comment = cleaned_data.get('comment')
        if comment and len(comment) < 5:
            self.add_error('comment', 'Комментарий должен быть не менее 5 символов')
        return cleaned_data