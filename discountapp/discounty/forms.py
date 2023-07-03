from django import forms
from .models import Store, Discount

class StoreRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    class Meta:
        model = Store
        fields = ['name', 'latitude', 'longitude', 'username', 'password', 'address', 'picture']

class StoreLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

class DiscountInputForm(forms.ModelForm):
    class Meta:
        model = Discount
        exclude = ['store']

class DiscountUpdateForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['original_price', 'discounted_price', 'code']


class DiscountDeleteForm(forms.Form):
    pass 