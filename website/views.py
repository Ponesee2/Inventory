from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
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

# def transaction_create(request):
#     """Process a new transaction (buying a product)."""
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             transaction = form.save(commit=False)  # Don't save yet
#             product = transaction.product

#             if transaction.units > product.available_units:
#                 messages.error(request, f"Not enough stock available for {product.name}.")
#             else:
#                 transaction.total_price = transaction.units * product.price  # Calculate price
#                 product.available_units -= transaction.units  # Deduct stock
#                 product.save()
#                 transaction.save()  # Save transaction

#                 messages.success(request, "Transaction successful!")
#                 return redirect('transaction_list')  # Redirect to transaction list

#     else:
#         form = TransactionForm()

#     return render(request, 'website/transaction_create.html', {'form': form})

def transaction_create(request):
    """Process a new transaction (buying a product)."""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            product = transaction.product

            if product.status == 'Unavailable' or product.available_units == 0:
                messages.error(request, f"{product.name} is out of stock and cannot be purchased.")
            elif transaction.units > product.available_units:
                messages.error(request, f"Not enough stock available for {product.name}.")
            else:
                transaction.total_price = transaction.units * product.price
                product.available_units -= transaction.units
                product.save()
                transaction.save()

                messages.success(request, "Transaction successful!")
                return redirect('transaction_list')

    else:
        form = TransactionForm()

    return render(request, 'website/transaction_create.html', {'form': form})

def transaction_list(request):
    """Show all transactions."""
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'website/transaction_list.html', {'transactions': transactions})