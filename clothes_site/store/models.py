from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.formfields import PhoneNumberField
from multiselectfield import MultiSelectField

from django.db import transaction
from django.core.exceptions import ValidationError

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(region='KG')
    address = models.CharField(max_length=150, null=True, blank=True)
    index_pochta = models.CharField(max_length=150, null=True, blank=True, verbose_name='почтовый индекс')

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class CategoryClothes(models.Model):
    category_name = models.CharField(max_length=32)# дублонка , курктка,

    def __str__(self):
        return f'{self.category_name}'


class PromoCategory(models.Model):#акция,хит продаж,тренд,колекция
    promo_category = models.CharField(max_length=32)
    time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.promo_category}'


class Clothes(models.Model):
    clothes_name = models.CharField(max_length=32)# толстовка
    category = models.ManyToManyField(CategoryClothes,  related_name='clothes_category')
    promo_category = models.ManyToManyField(PromoCategory, related_name='clothes_with_promo')
    SIZE_CHOICES = (
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL')
    )
    size = MultiSelectField(verbose_name='размер', choices=SIZE_CHOICES, null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    made_in = models.CharField(max_length=32)
    active = models.BooleanField(default=True, verbose_name='в наличии')
    clothes_photo = models.FileField(upload_to='clothes_video/', null=True, blank=True)
    quantities = models.PositiveSmallIntegerField()
    created_date = models.DateField(auto_created=True)

    def __str__(self):
        return f'{self.clothes_name} - {self.price}'

    def get_average_rating(self):
        ratings = self.clothes_review.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class Textile(models.Model):
    textile_name = models.CharField(max_length=35)
    textile_clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE,related_name='textile_clothes')


class Color(models.Model):
    color = models.CharField(max_length=25, unique=True)
    clothes_connect = models.ForeignKey(Clothes, on_delete=models.CASCADE, null=True, blank=True, related_name='color')

    def __str__(self):
        return f'{self.color}'


class Photo(models.Model):
    photo = models.FileField(upload_to='clothes_color_img/')
    clothes_photo = models.ForeignKey(Clothes, on_delete=models.CASCADE, related_name='clothes_img')
    color_connect = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color_photo')


class Review(models.Model):
    author = models.ForeignKey(UserProfile, related_name='user_review', on_delete=models.CASCADE)
    clothes_review = models.ForeignKey(Clothes, related_name='clothes_review', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг", null=True, blank=True)
    review_photo = models.ImageField(upload_to='review_img/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} - {self.clothes_review} - {self.stars}'



class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        return total_price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    size = models.CharField(max_length=25, choices=Clothes.SIZE_CHOICES)  # Размер
    color = models.ForeignKey(Color, on_delete=models.CASCADE)  # Цвет
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.clothes} - {self.quantity}'

    def get_total_price(self):
        return self.clothes.price * self.quantity


class Order(models.Model):
    order_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)#
    date = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('обработка', 'Oбработка'),
        ('в процессе доставки', 'в процессе доставки'),
        ('доставлен', 'Доставлен'),
        ('отменен', 'Отменен'),
    )
    order_status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='Oбработка')
    STATUS_DELIVERY = (
        ('курьер', 'курьер'),
        ('самовызов', 'самовызов'),
    )
    delivery = models.CharField(max_length=20, default='самовызов', choices=STATUS_DELIVERY)
    address = models.CharField(max_length=100)
    order_price = models.PositiveIntegerField()


    def __str__(self):
        return f'{self.order_user} - {self.order_status}'

    def save(self, *args, **kwargs):
        """
        Проверяет наличие достаточного количества товаров на складе для всех товаров в корзине,
        а также обновляет количество товара на складе при создании заказа.
        """
        with transaction.atomic():  # Используем транзакции для целостности данных
            # Получаем связанные с корзиной товары
            cart_items = self.cart.items.all()

            if not cart_items:
                raise ValidationError("Корзина пуста. Добавьте товары перед оформлением заказа.")

            # Проверяем количество каждого товара
            for cart_item in cart_items:
                clothes = cart_item.clothes
                if cart_item.quantity > clothes.quantities:
                    raise ValidationError(
                        f"Недостаточно товара: {clothes.clothes_name}."
                        f" В наличии {clothes.quantities}, запрошено {cart_item.quantity}."
                    )

            # Уменьшаем количество на складе
            for cart_item in cart_items:
                clothes = cart_item.clothes
                clothes.quantities -= cart_item.quantity
                clothes.save()

            # Рассчитываем общую стоимость заказа
            self.order_price = sum(cart_item.get_total_price() for cart_item in cart_items)

            super().save(*args, **kwargs)  # Сохраняем заказ

class Favorite(models.Model):
    favorite_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favorite_user')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.favorite_user}'


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, related_name='items', on_delete=models.CASCADE)
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, related_name='clothes_favorite')

    def __str__(self):
        return f'{self.clothes}'
