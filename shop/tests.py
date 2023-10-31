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
def test_update_category_get(category_with_permission):
    client = Client()
    client.force_login(category_with_permission.owner)
    data = {
        'name': 'test1',
        "description": 'test description'
    }
    url = reverse('update_category', args=(category_with_permission.id,))
    response = client.get(url, data)
    assert response.status_code == 302
    assert Category.objects.get(**data)



@pytest.mark.django_db
def test_update_category_post(category_with_permission):
    data = {'name': 'test', 'description': 'test'}
    client = Client()
    client.force_login(category_with_permission.owner)
    url = reverse('update_category', args=(category_with_permission.id,))
    response = client.post(url, data)
    assert response.status_code == 302

@pytest.mark.django_db
def test_order_list_view(user):
    # Create an instance of the client.
    client = Client()

    client.force_login(user)

    # Use the client to make a request to your view
    response = client.get(reverse('orders'))

    assert response.status_code == 403



@pytest.mark.django_db
def test_product(category):
    client = Client()
    url = reverse('list_product', args=(category.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert category == response.context['object']


@pytest.mark.django_db
def test_cart_detail_view(client, user, product, cart, cart_item):
    client.login(username='test', password='test')

    response = client.get(reverse('cart_detail'))

    assert response.status_code == 200  # Check if the page loaded successfully
    assert str(product.id) in str(response.content)  # Check if the product id is in the response


@pytest.mark.django_db
def test_add_product():
    data = {'name': 'test', 'description': 'test', 'price': 100}
    client = Client()
    url = reverse('add_product')
    response = client.post(url, data)
    assert response.status_code == 302
    Category.objects.get(**data)


@pytest.mark.django_db
def test_add_to_cart_view(client, user, product, cart):
    client.login(username='test', password='test')

    response = client.post(reverse('add_to_cart', kwargs={'product_id': product.id}), {'quantity': 2})

    assert response.status_code == 302  # Check if redirect happened
    assert CartItem.objects.filter(cart=cart, product_id=product.id).exists()  # Check if item was added to cart

    cart_item = CartItem.objects.get(cart=cart, product_id=product.id)
    assert cart_item.quantity == 2  # Check if quantity is correct


@pytest.mark.django_db
def test_AddProductView_get(category):
    client = Client()
    request = client.get('/shop/add_product/')
    view = AddProductView.as_view()
    response = view(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_AddProductView_post(product, category):
    client = Client()
    data = {
        'name': 'New Product',
        'price': 200,
        'description': 'New Description',
        'category': category.id,
    }
    request = client.post('/shop/add_product/', data)
    request.session = {}
    view = AddProductView.as_view()
    response = view(request)
    assert response.status_code == 302  # Check for redirect
    assert Product.objects.filter(name='New Product').exists()


@pytest.mark.django_db
def test_order_detail_view_get():
    # Create an instance of the client.
    client = Client()

    # Create a user and log them in
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')

    # Create an order and related objects for the test
    product = Product.objects.create(name='Test Product', description='test', price=100.0)
    order = Order.objects.create(user=user)
    order_item = OrderItem.objects.create(product=product, order=order, quantity=1)

    # Use the client to make a request to your view
    response = client.get(f'/path/to/view/{order.id}/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_order_detail_view_post(user):
    # Create an instance of the client.
    client = Client()

    # Create a user and log them in

    client.login(username='testuser', password='12345')

    # Create a cart and related objects for the test
    product = Product.objects.create(name='Test Product', description='test', price=100.0)
    cart = Cart.objects.create(user=user)
    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)

    # Use the client to make a request to your view
    response = client.post(f'/path/to/view/{cart.id}/')

    assert response.status_code == 302  # Check for redirect status code