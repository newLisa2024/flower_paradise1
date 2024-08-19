from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Order, Product

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    # Пример валидации для поля email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email уже используется")
        return email

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['products']

    # Пример добавления метода для обработки перед сохранением
    def save(self, commit=True):
        order = super().save(commit=False)
        # Здесь можно добавить логику, например, рассчитать общую стоимость заказа
        if commit:
            order.save()
        return order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'description']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'payment_method']
        labels = {
            'delivery_address': 'Адрес доставки',
            'payment_method': 'Способ оплаты',
        }
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
        }
