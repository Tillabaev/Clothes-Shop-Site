from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *
from django.db.models import Avg


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileAllSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.queryset.user)


# class ClothesColorListAPIView(generics.ListAPIView):
#     queryset = ClothesImg.objects.all()
#     serializer_class = ClothesColorSerializer


class ClothesListAPIView(generics.ListAPIView):
    queryset = Clothes.objects.annotate(avg_rating=Avg('clothes_review__stars'))  # Добавляем аннотацию для среднего рейтинга
    serializer_class = ClothesListSerializer
    filter_backends = [OrderingFilter]
    search_fields = ['clothes_name']
    ordering_fields = ['avg_rating', 'price', 'created_date']  # Поля для сортировки
    ordering = ['-avg_rating']  # Сортировка по убыванию популярности (по умолчанию)


class CategoryListAPIView(generics.ListAPIView):
    queryset = CategoryClothes.objects.all()
    serializer_class = CategoryClothesSerializer


class PromoCategoryListAPIView(generics.ListAPIView):
    queryset = PromoCategory.objects.all()
    serializer_class = PromoCategorySerializer


class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewSerializer


class CartCreateAPIView(generics.CreateAPIView):
    serializer_class = CartSimpleSerializer


class CartListAPIView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['clothes_name']
    ordering_fields = ['price']


    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemCreateAPIView(generics.CreateAPIView):#?
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class CartItemUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return Order.objects.all()


class OrderDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.queryset.user)


class ClothesDetailViewSet(generics.RetrieveAPIView):
    queryset = Clothes.objects.all()
    serializer_class = ClothesDetailSerializer
    search_fields = ['clothes_name']
    ordering_fields = ['price']


class FavoriteViewSet(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteItemViewSet(generics.CreateAPIView):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer


class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            cart_item = serializer.save(user=request.user)
            return Response(
                {
                    "message": f"{cart_item.clothes.clothes_name} добавлен в корзину.",
                    "item": {
                        "id": cart_item.id,
                        "clothes": cart_item.clothes.clothes_name,
                        "color": cart_item.color,
                        "size": cart_item.size,
                        "quantity": cart_item.quantity,
                        "total_price": cart_item.get_total_price(),
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartListSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart