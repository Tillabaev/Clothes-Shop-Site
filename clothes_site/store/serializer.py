from phonenumbers.unicode_util import Category
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError


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
        fields = ['photo']


class ClothesColorSerializer(serializers.ModelSerializer):
    color_photo = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Color
        fields = ['color', 'color_photo']


class ClothesListSerializer(serializers.ModelSerializer):
    promo_category = PromoCategorySimpleSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    color = ClothesColorSerializer(read_only=True, many=True)

    class Meta:
        model = Clothes
        fields = ['clothes_photo', 'promo_category', 'clothes_name', 'price', 'size', 'color',  'average_rating']

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
    time = serializers.DateTimeField(format('%h-%m-%Y  %H:%M'))

    class Meta:
        model = PromoCategory
        fields = ['promo_category', 'time', 'clothes_with_promo']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['author', 'text', 'stars', 'review_photo', 'clothes_review']


class ReviewReadSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer()
    created_date = serializers.DateTimeField(format('%h-%m-%Y  %H:%M'))

    class Meta:
        model = Review
        fields = ['author', 'text', 'stars', 'review_photo', 'created_date']


class CartSimpleSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Cart
        fields = ['user',]


class CartItemSerializer(serializers.ModelSerializer):
    clothes = ClothesListSerializer(read_only=True)
    clothes_id = serializers.PrimaryKeyRelatedField(queryset=Clothes.objects.all(), write_only=True, source='clothes')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['clothes', 'clothes_id', 'quantity', 'total_price', 'color', 'size']

    def get_total_price(self, obj):
        return obj.get_total_price()


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
        fields = ['order_user', 'address', 'delivery']


class TextileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Textile
        fields = ['textile_name']


class ClothesDetailSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(many=True)
    promo_category = PromoSimpleSerializer(many=True)
    color = ClothesColorSerializer(read_only=True, many=True)
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
        fields = ['favorite', 'clothes']


class AddToCartSerializer(serializers.Serializer):
    clothes_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    color = serializers.CharField(max_length=32)
    size = serializers.CharField(max_length=4)

    def validate(self, data):
        try:
            clothes_item = Clothes.objects.get(pk=data['clothes_id'])
            if not clothes_item.active or clothes_item.quantities < data['quantity']:
                raise serializers.ValidationError("Недостаточно товара на складе.")
        except Clothes.DoesNotExist:
            raise serializers.ValidationError("Товар не найден.")
        return data

    def save(self, **kwargs):
        user = kwargs['user']
        cart, created = Cart.objects.get_or_create(user=user)
        clothes_item = Clothes.objects.get(pk=self.validated_data['clothes_id'])
        quantity = self.validated_data['quantity']
        color = self.validated_data.get('color')  # Убедитесь, что поле 'color' передано
        size = self.validated_data.get('size')


        cart_item, created = CartItem.objects.get_or_create(cart=cart, clothes=clothes_item,
                                                            color=color, size=size)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        clothes_item.quantities -= quantity
        clothes_item.save()

        return cart_item
