from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView, FormView

from django.contrib.auth.models import User

from shop.models import Category, Product, Cart, CartItem, Order, OrderItem
from shop.forms import AddProduct


# Create your views here.
class BaseView(View):

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'base.html', {'categories': categories, })


class AddCategoryView(PermissionRequiredMixin, View):
    permission_required = 'shop.add_category'

    def get(self, request):
        category = Category.objects.all()
        return render(request, 'add_category.html', {'category': category, })

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        Category.objects.create(name=name, description=description)
        return redirect('index')


class ListCategoryView(ListView):
    model = Category
    template_name = 'base.html'


def search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        results = Product.objects.all()
    return render(request, 'search_results.html', {'results': results})


class DeleteCategoryView(PermissionRequiredMixin, DeleteView):
    permission_required = 'shop.delete_category'
    model = Category
    template_name = 'delete_category_form.html'
    success_url = reverse_lazy('index')

    def has_permission(self):
        has_perms = super().has_permission()
        self.object = self.get_object()
        return has_perms




class UpdateCategoryView(PermissionRequiredMixin, UpdateView):
    permission_required = 'shop.change_category'
    model = Category
    fields = '__all__'
    template_name = 'add_category.html'
    success_url = reverse_lazy('index')


class AddProductView(PermissionRequiredMixin, View):
    permission_required = 'shop.add_product'

    def get(self, request):
        form = AddProduct()
        return render(request, 'add_product.html', {'form': form})

    def post(self, request):
        form = AddProduct(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            Product.objects.create(name=name, category=category, price=price, description=description)
            return redirect('/shop/add_product/')
        else:
            return render(request, 'add_product.html', {'form': form})


class ListProductView(ListView):
    model = Product
    template_name = 'list_product.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Product.objects.filter(category__name=category)


class DeleteProductView(PermissionRequiredMixin, DeleteView):
    permission_required = 'delete_product'
    model = Product
    template_name = 'delete_product_form.html'
    success_url = reverse_lazy('index')

    def has_permission(self):
        has_perms = super().has_permission()
        self.object = self.get_object()
        return has_perms


class UpdateProductView(PermissionRequiredMixin, UpdateView):
    permission_required = 'shop.add_product'
    model = Product
    fields = '__all__'
    template_name = 'add_product.html'
    success_url = reverse_lazy('index')

    def has_permission(self):
        has_perms = super().has_permission()
        self.object = self.get_object()
        return has_perms

    # get or creatre


class CartDetailView( LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs, ):
        user = request.user
        orders = Order.objects.filter(user=user)
        cart, created = Cart.objects.get_or_create(user=user)

        cart_items = CartItem.objects.filter(cart=cart)

        if orders.exists():
            order = orders.last()
        else:
            order = Order.objects.create(user=user)

        total_price = sum(item.product.price * item.quantity for item in cart_items)


        order_id = order.id

        return render(request, 'cart.html', {'cart_items': cart_items, 'order_id': order_id, 'total_price': total_price})


class AddToCartView(View):

    def get(self, request, product_id):
        return render(request, 'add_to_cart.html', {'product_id': product_id})

    def post(self, request, product_id):
        user = request.user
        quantity = int(request.POST.get('quantity'))

        cart, created = Cart.objects.get_or_create(user=user)

        cart_item, created = CartItem.objects.get_or_create(
            product_id=product_id,
            cart=cart,
            defaults={'quantity': quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cart')


class OrderListView(PermissionRequiredMixin, View):
    permission_required = 'shop.view_order'

    def get(self, request):
        orders = Order.objects.all()
        return render(request, 'orders.html', {'orders': orders, })


class OrderDetailView(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        order = Order.objects.get(id=order_id)
        order_items = order.orderitem_set.all()
        total_price = sum(item.product.price * item.quantity for item in order_items)
        return render(request, 'order_detail.html', {'order_items': order_items, 'total_price' : total_price})

    def post(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        order = Order.objects.create(user=user)

        for item in CartItem.objects.filter(cart=cart):
            OrderItem.objects.create(
                product=item.product,
                order=order,
                quantity=item.quantity,
            )

        cart.delete()

        return redirect('order_detail', order_id=order.id)
