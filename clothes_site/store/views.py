from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets, status,permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import *


class AddToCartView(APIView):


    def post(self, request, clothes_id):
        size = request.data.get('size')  # Получаем выбранный размер
        color_id = request.data.get('color')  # Получаем выбранный цвет

        if not size or not color_id:
            return Response({"detail": "Size and color must be selected."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            color = Color.objects.get(id=color_id)
            clothes = Clothes.objects.get(id=clothes_id)
        except (Color.DoesNotExist, Clothes.DoesNotExist):
            return Response({"detail": "Invalid color or clothes ID."}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.create(cart=cart, product=clothes, size=size, color=color)

        return Response({"detail": "Item added to cart."}, status=status.HTTP_201_CREATED)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

class CreateOrderView(APIView):
    def post(self, request):
        try:
            user = request.user
            address = request.data.get('address', '')
            delivery = request.data.get('delivery', 'самовызов')

            if not address:
                return Response({"detail": "Address is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Создаем заказ
            order = Order.objects.create(order_user=user, address=address, delivery=delivery)
            return Response({"detail": "Order created successfully."}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class OrderCheckList(generics.ListAPIView):
    serializer_class = OrderCheckSerializer

    def get_queryset(self):
        return Order.objects.filter(order_user = self.request.user)



class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileAllSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.queryset.user)


class ClothesListAPIView(generics.ListAPIView):
    queryset = Clothes.objects.all()
    serializer_class = ClothesListSerializer
    filter_backends = [OrderingFilter]
    search_fields = ['clothes_name']
    permission_classes = [permissions.IsAuthenticated]

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


class FavoriteViewSet(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteItemViewSet(generics.CreateAPIView):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer

