
import pytest
from django.contrib.auth.models import User, Permission

from shop.models import Category, Product, Cart, CartItem


@pytest.fixture
def category():
    c = Category.objects.create(
        name='test',
        description='test',
    )
    return c



@pytest.fixture
def user():
    u = User.objects.create(username='testuser')
    return u
@pytest.fixture
def user_with_permission(user):
    p = Permission.objects.get(codename='change_category')
    user.user_permissions.add(p)
    return user

@pytest.fixture
def category_with_permission(user_with_permission):
    cat = Category.objects.create(
        name='test',
        description='test',
        owner=user_with_permission
    )
    return cat

@pytest.fixture
def product():
    return Product.objects.create(name='Test Product',description='test', price=10)

@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user)

@pytest.fixture
def cart_item(cart, product):
    return CartItem.objects.create(cart=cart, product_id=product.id, quantity=2)

@pytest.fixture
def category():
    return Category.objects.create(name='Test Category', description='Test Description')

@pytest.fixture
def product(category):
    return Product.objects.create(name='Test Product', price=100, description='Test Description', category=category)