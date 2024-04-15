# Generated by Django 4.0.4 on 2022-06-27 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_rename_permalink_product_permalink'),
        ('home', '0003_homesectionone'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeSectionTwo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_title', models.CharField(max_length=160)),
                ('products', models.ManyToManyField(to='products.product')),
            ],
        ),
    ]
