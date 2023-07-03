from django.shortcuts import render, redirect, get_object_or_404
from .forms import StoreRegistrationForm, StoreLoginForm, DiscountInputForm
from .models import Store, Discount
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib import auth


# Create your views here.
def register_store(request):
    if request.method == 'POST':
        form = StoreRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.password = make_password(form.cleaned_data['password'])
            store.save()
            return redirect('home')
    else:
        form = StoreRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_store(request):
    if request.method == 'POST':
        form = StoreLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                store = Store.objects.get(username=username)
            except Store.DoesNotExist:
                return redirect('login')
            
            if check_password(password, store.password):
                request.session['store_id'] = store.id
                return redirect('dashboard')
            else:
                return redirect('login')
    else:
        form = StoreLoginForm()
    
    return render(request, 'index.html', {'form': form})




def dashboard(request):
    store_id = request.session.get('store_id')
    store = Store.objects.get(id=store_id)
    return render(request, 'discount_list.html', {'store': store})
    
class DiscountUpdateView(UpdateView):
    model = Discount
    template_name = 'discount_update.html'
    fields = ['url', 'original_price', 'discounted_price', 'code']

    def get_success_url(self):
        return reverse_lazy('dashboard')  # Redirect to the discount list page after successful update

class DiscountDeleteView(DeleteView):
    model = Discount
    template_name = 'discount_delete.html'
    success_url = reverse_lazy('dashboard')  # Redirect to the discount list page after successful deletion


def add_discount(request):
    if request.method == 'POST':
        form = DiscountInputForm(request.POST)
        if form.is_valid():
            discount = form.save(commit=False)
            store_id = request.session.get('store_id')
            store = Store.objects.get(id=store_id)
            discount.store = store
            discount.save()
            return redirect('dashboard')
    else:
        form = DiscountInputForm()
    return render(request, 'create_discount.html', {'form': form})



def discount_list(request):
    store_id = request.session.get('store_id')
    store = Store.objects.get(id=store_id)
    discounts = store.discount_set.all()
    return render(request, 'discount_list.html', {'store': store, 'discounts': discounts})


def logout_store(request):
    logout(request)
    return redirect('login')