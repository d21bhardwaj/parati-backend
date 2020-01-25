# Generated by Django 2.2.5 on 2019-11-12 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userapi', '0012_userfeedback_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_size',
            name='availability',
        ),
        migrations.AddField(
            model_name='product_attribute',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='attribute_category', to='userapi.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product_size',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='size_category', to='userapi.Category'),
            preserve_default=False,
        ),
    ]
