# Generated by Django 4.0.4 on 2022-06-15 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(blank=True, default='static/images/account/default_profile.png', null=True, upload_to='static/images/account/profile_img'),
        ),
    ]