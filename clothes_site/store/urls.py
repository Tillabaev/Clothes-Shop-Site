from django.urls import path
from .views import *

urlpatterns = [
    #default register
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #cookie
    path('api/login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('api/logout/', LogoutCookieView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', ClothesListAPIView.as_view(), name='clothes_list'),

    path('<int:pk>/', ClothesDetailViewSet.as_view(), name='clothes_detail'),

    path('category/', CategoryListAPIView.as_view(), name='category_clothes'),

    path('promo/', PromoCategoryListAPIView.as_view(), name='promo_clothes'),

    path('review_add/', ReviewCreateAPIView.as_view(), name='review_add'),

    path('cart_create/', CartCreateAPIView.as_view(), name='cart_create'),


    path('cart-list/', CartListAPIView.as_view(), name='cart-list'),

    path('cart_item/create/', CartItemCreateAPIView.as_view(), name='cart_item_create'),

    path('cart_item/<int:pk>/', CartItemUpdateDeleteApiView.as_view(), name='cart_item_delete'),

    path('favorite/', FavoriteViewSet.as_view(), name='favorite'),
    path('favorite_item/', FavoriteItemViewSet.as_view(), name='favorite_item'),

    path('cart_item/add/<int:clothes_id>/', AddToCartView.as_view(), name='cart_add_test'),

    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailViewSet.as_view(), name='order-detail'),



]