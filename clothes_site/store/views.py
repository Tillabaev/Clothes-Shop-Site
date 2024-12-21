from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileAllSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.queryset.user)


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

    @action(detail=False, methods=['get'])
    def by_color(self, request):
        # Түс боюнча кийимдерди фильтровать кылуу
        color_id = request.query_params.get('color', None)
        if color_id is not None:
            clothes = Clothes.objects.filter(colors__id=color_id)
            serializer = ClothesDetailSerializer(clothes, many=True)
            return Response(serializer.data)
        return Response({"error": "Color parameter is required."}, status=400)


class FavoriteViewSet(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
