# Generated by Django 4.0.4 on 2022-07-02 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_product_product_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_img',
            field=models.ImageField(blank=True, null=True, upload_to='category_img'),
        ),
        migrations.AlterField(
            model_name='color',
            name='color_img',
            field=models.ImageField(upload_to='color_img'),
        ),
    ]
