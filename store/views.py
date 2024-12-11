from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileAllSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.queryset.user)


# class ClothesColorListAPIView(generics.ListAPIView):
#     queryset = ClothesImg.objects.all()
#     serializer_class = ClothesColorSerializer


class ClothesListAPIView(generics.ListAPIView):
    queryset = Clothes.objects.all()
    serializer_class = ClothesListSerializer
    search_fields = ['clothes_name']
    ordering_fields = ['price']



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


# class OrderCreateView(generics.CreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#
#     def post(self, request, *args, **kwargs):
#         clothes_id = request.data.get('clothes_id')  # ID товара
#         quantity_order = request.data.get('quantity_order')  # Количество товара в заказе
#
#         try:
#             clothes = Clothes.objects.get(id=clothes_id)
#         except Clothes.DoesNotExist:
#             return Response({"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)
#
#         if quantity_order > clothes.quantity:
#             return Response(
#                 {"message": f"У нас осталось только {clothes.quantity} штук"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         elif quantity_order == clothes.quantity:
#             # Создаем заказ
#             Order.objects.create(quantity_order=quantity_order, clothes=clothes)
#             # Обновляем количество товара в базе
#             clothes.quantity = 0
#             clothes.save()
#             return Response({"message": "Заказ выполнен успешно"}, status=status.HTTP_201_CREATED)
#         else:
#             # Создаем заказ
#             Order.objects.create(quantity_order=quantity_order, clothes=clothes)
#             # Обновляем количество товара в базе
#             clothes.quantity -= quantity_order
#             clothes.save()
#             return Response({"message": "Заказ выполнен успешно"}, status=status.HTTP_201_CREATED)


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


