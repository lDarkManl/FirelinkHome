# Generated by Django 4.1 on 2023-03-16 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='image',
            field=models.ImageField(upload_to='images/music/%Y/%m/%d/', verbose_name='Изображение'),
        ),
    ]
