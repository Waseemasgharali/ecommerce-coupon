# Generated by Django 4.0.4 on 2022-06-25 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_category_category_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_img',
            field=models.ImageField(blank=True, null=True, upload_to='static/images/product/category'),
        ),
    ]
