from django.urls import path
from products import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('/create', views.ProductCreateView.as_view(), name='product_create'),
    path('/<int:pk>/update', views.ProductUpdateView.as_view(), name='product_update'),
    path('/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product_delete'),
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/', views.view_cart, name='cart'),
    path('increase-cart-item/<int:product_id>/', views.increase_cart_item, name='increase_cart_item'),
    path('decrease-cart-item/<int:product_id>/', views.decrease_cart_item, name='decrease_cart_item'),
]