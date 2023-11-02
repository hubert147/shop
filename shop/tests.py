import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from shop.models import Category, Product, CartItem, Cart, OrderItem, Order
from shop.views import AddProductView


# Create your tests here.
@pytest.mark.django_db
def test_index_view():
    client = Client()
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_category(category):
    client = Client()
    url = reverse('category', args=(category.id,))
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_category():
    data = {'name': 'test', 'description': 'test'}
    client = Client()
    url = reverse('add_category')
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_category_post_without_perm(category, user_with_permission_change_cat):
    client = Client()
    client.force_login(user_with_permission_change_cat)
    data = {
        'name': 'test1',
        "description": 'test1'
    }
    url = reverse('update_category', args=(category.id,))
    response = client.post(url, data)
    assert response.status_code == 302
    assert Category.objects.get(**data)


@pytest.mark.django_db
def test_delete_category_view_get_with_perm(user_with_permission_delete_cat, category):
    client = Client()
    response = client.get(reverse('delete_category', args=[category.id]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_category_post(user, category):
    data = {'name': 'test', 'description': 'test'}
    client = Client()
    client.force_login(user)
    url = reverse('update_category', args=(category.id,))
    response = client.post(url, data)
    assert response.status_code == 403

@pytest.mark.django_db
def test_update_category_post(user_with_permission_change_cat, category):
    data = {'name': 'test', 'description': 'test'}
    client = Client()
    client.force_login(user_with_permission_change_cat)
    url = reverse('update_category', args=(category.id,))
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_product_get_without_perm(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_product')
    response = client.get(url)
    assert response.status_code == 403
@pytest.mark.django_db
def test_add_product_get_with_perm(user_with_permission_add_product):
    client = Client()
    client.force_login(user_with_permission_add_product)
    url = reverse('add_product')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_product_post_without_perm(user, category):
    client = Client()
    client.force_login(user)
    url = reverse('add_product')
    data = {
        'name':'testName',
        'description':'testDis',
        'price':100,
        'category': category.id
    }
    response = client.post(url, data)
    assert response.status_code == 403

@pytest.mark.django_db
def test_add_product_post_with_perm(user_with_permission_add_product, category):
    client = Client()
    client.force_login(user_with_permission_add_product)
    url = reverse('add_product')
    data = {
        'name':'testName',
        'description':'testDis',
        'price':100,
        'category':category.id
    }
    response = client.post(url, data)
    assert response.status_code == 302



@pytest.mark.django_db
def test_product_list_view(category):
    client = Client()
    url = reverse('list_product', args=(category.id,))
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_product_get_with_perm(user_with_permission_delete_product, product):
    client = Client()
    client.force_login(user_with_permission_delete_product)
    url = reverse('delete_product', args=(product.id,))
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_product_view_get_with_perm(user_with_permission_delete_product, category):
    client = Client()
    response = client.post(reverse('delete_product', args=[category.id]))
    assert response.status_code == 302

@pytest.mark.django_db
def test_update_product_get_without_perm(user, product):
    client = Client()
    client.force_login(user)
    url = reverse('update_product', args=(product.id, ))
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_update_product_get_with_perm(user_with_permission_change_product, product):
    client = Client()
    client.force_login(user_with_permission_change_product)
    url = reverse('update_product', args=(product.id, ))
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_product_post_without_perm(category, user_with_permission_change_product, product):
    client = Client()
    client.force_login(user_with_permission_change_product)
    url = reverse('update_product', args=(product.id,))
    data = {
        'name': 'test1',
        "description": 'test1',
        'price': 120,

    }

    response = client.post(url, data)
    assert response.status_code == 403






@pytest.mark.django_db
def test_order_list_view_with_perm(user_with_permission_view_order):
    client = Client()
    client.force_login(user_with_permission_view_order)
    url = reverse('orders')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_cart_view_without_login(cart):
    client = Client()
    url = reverse('cart')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_order_list_view_without_perm(user):
    client = Client()
    client.force_login(user)
    url = reverse('orders')
    response = client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_add_to_cart_view_get(user, product):
    client = Client()
    client.force_login(user)
    url = reverse('add_to_cart', args=(product.id,))
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_to_cart_view_post( user, product, cart):
    client = Client()
    client.force_login(user)
    data = {
        'product_id' : product.id,
        'cart' : cart,
        'quantity': 2,
    }
    url = reverse('add_to_cart',args=(product.id,))
    response = client.post(url, data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_order_detail_view_get( user, order):
    client = Client()
    client.force_login(user)
    response = client.get(reverse('order_detail', args=(order.id,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_detail_view_post(user, order):
    client = Client()
    client.force_login(user)
    url = reverse('order_detail', args=[order.id, ])
    response = client.get(url)
    assert response.status_code == 200















