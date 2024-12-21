# Generated by Django 5.1.3 on 2024-12-21 09:58

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryClothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_category', models.CharField(max_length=32)),
                ('time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('index_pochta', models.CharField(blank=True, max_length=150, null=True, verbose_name='почтовый индекс')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_created=True)),
                ('clothes_name', models.CharField(max_length=32)),
                ('size', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], max_length=17, null=True, verbose_name='размер')),
                ('price', models.PositiveIntegerField(default=0)),
                ('made_in', models.CharField(max_length=32)),
                ('active', models.BooleanField(default=True, verbose_name='в наличии')),
                ('clothes_photo', models.FileField(blank=True, null=True, upload_to='clothes_video/')),
                ('quantities', models.PositiveSmallIntegerField()),
                ('category', models.ManyToManyField(related_name='clothes_category', to='store.categoryclothes')),
                ('promo_category', models.ManyToManyField(related_name='clothes_with_promo', to='store.promocategory')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=25, unique=True)),
                ('clothes_connect', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='color', to='store.clothes')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], max_length=25)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.cart')),
                ('clothes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.clothes')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.color')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('favorite_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clothes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clothes_favorite', to='store.clothes')),
                ('favorite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.favorite')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('order_status', models.CharField(choices=[('обработка', 'Oбработка'), ('в процессе доставки', 'в процессе доставки'), ('доставлен', 'Доставлен'), ('отменен', 'Отменен')], default='Oбработка', max_length=32)),
                ('delivery', models.CharField(choices=[('курьер', 'курьер'), ('самовызов', 'самовызов')], default='самовызов', max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('order_price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.cartitem')),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.FileField(upload_to='clothes_color_img/')),
                ('clothes_photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clothes_img', to='store.clothes')),
                ('color_connect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_photo', to='store.color')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('stars', models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='Рейтинг')),
                ('review_photo', models.ImageField(blank=True, null=True, upload_to='review_img/')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_review', to=settings.AUTH_USER_MODEL)),
                ('clothes_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clothes_review', to='store.clothes')),
            ],
        ),
        migrations.CreateModel(
            name='Textile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('textile_name', models.CharField(max_length=35)),
                ('textile_clothes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='textile_clothes', to='store.clothes')),
            ],
        ),
    ]
