# Generated by Django 4.1 on 2022-10-21 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smr', '0004_alter_user_benchpress_alter_user_body_fat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics'),
        ),
    ]
