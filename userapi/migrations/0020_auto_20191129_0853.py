# Generated by Django 2.2.5 on 2019-11-29 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapi', '0019_auto_20191118_0349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_images',
            name='image_url',
            field=models.CharField(max_length=1000),
        ),
    ]