from django.urls import path
from shop import views


urlpatterns = [

    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<int:pk>/', views.ListCategoryView.as_view(), name='category'),
    path('add_product/', views.AddProductView.as_view(), name='add_product'),
    path('delete_category/<int:pk>/', views.DeleteCategoryView.as_view(), name='delete_category'),
    path('update_category/<int:pk>/', views.UpdateCategoryView.as_view(), name='update_category'),
    path('products/<str:category>/', views.ListProductView.as_view(), name='list_product'),
    path('delete_product/<int:pk>/', views.DeleteProductView.as_view(), name='delete_product'),
    path('update_product/<int:pk>/', views.UpdateProductView.as_view(), name='update_product'),
    path('add_to_cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartDetailView.as_view(), name='cart'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('search/', views.search, name='search'),
]