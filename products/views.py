from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Product, Cart, CartItem
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    ) 
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()
        context['products'] = all_products.order_by('created_on').reverse()
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('product_list')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/product_update.html'
    success_url = reverse_lazy('product_list')
    fields = ['title', 'description', 'price', 'image']
    
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_delete.html'
    success_url = reverse_lazy('product_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context
    
class ProductSearchView(ListView):
    model = Product
    template_name = 'products/product_search.html'
    context_object_name = 'products'
    paginate_by = 10
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(title__icontains=query)
        else:
            return Product.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        
        return context

# Cart Functionality 

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    size = request.POST.get('size') 
    quantity = int(request.POST.get('quantity', 1))

    # Check if a cart item with the same product and size already exists
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size  # Include size in the uniqueness check
    )
    
    if not item_created:
        # If the item already exists, increase the quantity
        cart_item.quantity += quantity
    else:
        # If the item is newly created, set the quantity
        cart_item.quantity = quantity

    cart_item.save()

    return redirect('product_list')

def remove_from_cart(request, product_id):
    size = request.POST.get('size')  # Get the size from the request, default to 'medium'
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = cart.cartitem_set.get(product=product, cart=cart, size=size)  # Ensure we match the size as well
        # Only delete if the quantity is 1, otherwise just decrease the quantity
        if cart_item.quantity >= 1:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')

def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    
    return render(request, 'products/cart.html', {'cart_items': cart_items})

def increase_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = cart.cartitem_set.get(product=product)
    cart_item.quantity += 1
    cart_item.save()
    
    return redirect('cart')

def decrease_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = cart.cartitem_set.get(product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')