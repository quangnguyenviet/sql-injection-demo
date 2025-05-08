from django.urls import path
from .views import (
    login_view, register_view, update_password_view, search,
    product_list, product_detail, create_order, order_list, add_comment
)

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('update-password/', update_password_view, name='update_password'),
    path('search/', search, name='search'),
    
    # URLs cho sản phẩm
    path('products/', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    
    # URLs cho đơn hàng
    path('orders/', order_list, name='order_list'),
    path('create-order/', create_order, name='create_order'),
    
    # URL cho bình luận
    path('add-comment/', add_comment, name='add_comment'),
]
