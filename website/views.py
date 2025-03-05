from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *

# Create your views here.
def dashboard (request):
    return render(request, 'website/dashboard.html', {} )

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'website/supplier_list.html', {'suppliers': suppliers})

# Create a new supplier
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier')
    else:
        form = SupplierForm()
    return render(request, 'website/supplier_form.html', {'form': form})

# Update an existing supplier
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'website/supplier_form.html', {'form': form})

# Delete a supplier
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'website/supplier_delete.html', {'supplier': supplier})

def product_list(request):
    product = Product.objects.all()
    return render(request, 'website/product_list.html', {'product': product})


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'website/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'website/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'website/product_delete.html'
    success_url = reverse_lazy('product_list')