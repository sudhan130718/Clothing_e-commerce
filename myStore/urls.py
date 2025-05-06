from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('categories/', views.category_page, name='category_page'),
    path('category/<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.product_detail,name='product_detail'),
    # cart
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-quantity/<int:item_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('remove-item/<int:item_id>/', views.remove_item, name='remove_item'),
     # checkout 
    path('checkout/', views.checkout, name='checkout'),

    # order
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
   ]
    


