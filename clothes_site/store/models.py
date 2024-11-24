from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.formfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(region='KG')

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=32)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=32)
    color = models.CharField(max_length=32)
    size = models.CharField(max_length=16, verbose_name='размер')
    price = models.PositiveIntegerField()
    category_ = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    textile = models.CharField(max_length=32, verbose_name='ткань')
    made_in = models.CharField(max_length=32)
    quantity = models.PositiveSmallIntegerField(default=1)
    active = models.BooleanField(default=True, verbose_name='в наличии')

    def __str__(self):
        return f'{self.product_name} - {self.price}'

    def get_average_rating(self):
        ratings = self.product_review.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')


class Review(models.Model):
    review_user = models.ForeignKey(UserProfile, related_name='user_review',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_review', on_delete=models.CASCADE)
    text = models.TextField()
    stars = models.IntegerField(choices=[(i, str(1)) for i in range(1, 6)], verbose_name="Рейтинг")

    def __str__(self):
        return f'{self.review_user} - {self.product} - {self.stars}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'{self.user}'


class CarItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product} - {self.quantity}'

    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        discount = 0


class Order(models.Model):
    order_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    car_item = models.ForeignKey(CarItem, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('обработка', 'Oбработка'),
        ('в процессе доставки', 'в процессе доставки'),
        ('доставлен', 'Доставлен'),
        ('отменен', 'Отменен'),
    )
    order_status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='Oбработка')

    def __str__(self):
        return f'{self.order_user} - {self.order_status}'


class History(models.Model):
    history_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='history', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.history_user} - {self.product} - {self.viewed_at} "


class Favorite(models.Model):
    favorite_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favorite_user')
    product = models.ForeignKey(Product, related_name='favorite_product', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.favorite_user}'