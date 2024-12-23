
from rest_framework import serializers
from .models import *

class UserProfileAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'address', 'index_pochta']


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class PromoCategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCategory
        fields = ['promo_category']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['photo', 'color_connect']


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ['color']


class ClothesListSerializer(serializers.ModelSerializer):
    promo_category = PromoCategorySimpleSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    color = ColorSerializer(many=True)
    # created_date = serializers.DateField(format('%d%m%Y'))
    class Meta:
        model = Clothes
        fields = ['id','clothes_photo', 'promo_category', 'clothes_name', 'price', 'size', 'color',  'average_rating','created_date']

    def get_average_rating(self,obj):
        return obj.get_average_rating()


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryClothes
        fields = ['category_name']


class CategoryClothesSerializer(serializers.ModelSerializer):
    clothes_category = ClothesListSerializer(many=True)
    class Meta:
        model = CategoryClothes
        fields = ['category_name', 'clothes_category']


class PromoSimpleSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format('%h-%m-%Y  %H:%M'))

    class Meta:
        model = PromoCategory
        fields =['promo_category', 'time']


class PromoCategorySerializer(serializers.ModelSerializer):
    clothes_with_promo = ClothesListSerializer(many=True)

    class Meta:
        model = PromoCategory
        fields = ['promo_category', 'time', 'clothes_with_promo']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['author', 'text', 'stars', 'review_photo', 'clothes_review']


class ReviewReadSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer()
    created_date = serializers.DateTimeField(format('%d-%m-%Y  %H:%M'))

    class Meta:
        model = Review
        fields = ['author', 'text', 'stars', 'review_photo', 'created_date']


class CartSimpleSerializer(serializers.ModelSerializer):


    class Meta:
        model = Cart
        fields = ['user',]


class CartItemSerializer(serializers.ModelSerializer):
    clothes = ClothesListSerializer(read_only=True)
    clothes_id = serializers.PrimaryKeyRelatedField(queryset=Clothes.objects.all(), write_only=True, source='clothes')

    class Meta:
        model = CartItem
        fields = ['clothes', 'clothes_id', 'quantity']




class CartListSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'user',  'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_user', 'cart', 'date',
                  'delivery', 'address', 'payment_method']

    def create(self, validated_data):
        return Order.objects.create(**validated_data)        # Создаём объект заказа


class TextileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Textile
        fields = ['textile_name']


class ClothesDetailSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(many=True)
    promo_category = PromoSimpleSerializer(many=True)
    color = ColorSerializer(read_only=True, many=True)
    clothes_review = ReviewReadSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    textile_clothes = TextileSerializer(read_only=True, many=True)

    class Meta:
        model = Clothes
        fields = ['clothes_name', 'clothes_photo', 'category',
                  'promo_category', 'quantities', 'active', 'price', 'size', 'average_rating',
                  'made_in', 'textile_clothes', 'color', 'clothes_review',]

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['favorite_user', 'created_date']


class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = ['cart', 'clothes']
