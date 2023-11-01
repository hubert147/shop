
import pytest
from django.contrib.auth.models import User, Permission

from shop.models import Category, Product, Cart, CartItem, Order, OrderItem


@pytest.fixture
def category():
    c = Category.objects.create(
        name='test',
        description='test',
    )
    return c
@pytest.fixture
def product(category):
    p = Product.objects.create(
        name='test',
        description='test',
        price= 100,
        category= category.name
    )
    return p


@pytest.fixture
def user():
    u = User.objects.create(username='testuser')
    return u

@pytest.fixture
def user_with_permission_change_cat(user):
    p = Permission.objects.get(codename='change_category')
    user.user_permissions.add(p)
    return user

@pytest.fixture
def user_with_permission_view_order(user):
    p = Permission.objects.get(codename='view_order')
    user.user_permissions.add(p)
    return user

@pytest.fixture
def user_with_permission_add_product(user):
    p = Permission.objects.get(codename='add_product')
    user.user_permissions.add(p)
    return user
@pytest.fixture
def user_with_permission_delete_cat(user):
    p = Permission.objects.get(codename='delete_category')
    user.user_permissions.add(p)
    return user

@pytest.fixture
def user_with_permission_delete_product(user):
    p = Permission.objects.get(codename='delete_product')
    user.user_permissions.add(p)
    return user

@pytest.fixture
def user_with_permission_change_product(user):
    p = Permission.objects.get(codename='change_product')
    user.user_permissions.add(p)
    return user


@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user)

@pytest.fixture
def cart_item(cart, product):
    return CartItem.objects.create(cart=cart, product_id=product.id, quantity=2)



@pytest.fixture
def order(user, product):
    order = Order.objects.create(user=user)
    OrderItem.objects.create(order=order, product=product, quantity=1)
    return order