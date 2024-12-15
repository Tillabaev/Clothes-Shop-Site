from django.urls import path
from .views import *

urlpatterns = [
    path('', ClothesListAPIView.as_view(), name='clothes_list'),

    path('<int:pk>/', ClothesDetailViewSet.as_view(), name='clothes_detail'),

    path('category/', CategoryListAPIView.as_view(), name='category_clothes'),

    path('promo/', PromoCategoryListAPIView.as_view(), name='promo_clothes'),

    path('review_add/', ReviewCreateAPIView.as_view(), name='review_add'),

    path('cart_simple/', CartCreateAPIView.as_view(), name='cart_simple'),

    path('order/<int:pk>/', OrderDetailViewSet.as_view(), name='order_detail'),

    path('cart-list/', CartListAPIView.as_view(), name='cart-list'),

    path('cart_item/create/', CartItemCreateAPIView.as_view(), name='cart_item_create'),

    path('cart_item/<int:pk>/', CartItemUpdateDeleteApiView.as_view(), name='cart_item_delete'),

    path('favorite/', FavoriteViewSet.as_view(), name='favorite'),

    path('favorite_item/', FavoriteItemViewSet.as_view(), name='favorite_item'),

    path('api/cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('api/cart/', CartDetailView.as_view(), name='cart-detail'),
]