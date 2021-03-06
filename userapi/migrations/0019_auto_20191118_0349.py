# Generated by Django 2.2.5 on 2019-11-18 03:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userapi', '0018_auto_20191118_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profile_address', to='userapi.UserAddress'),
        ),
        migrations.CreateModel(
            name='UserSecondaryPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_type', models.CharField(max_length=50)),
                ('t_size', models.CharField(max_length=50)),
                ('t_fit', models.CharField(max_length=50)),
                ('b_size', models.CharField(max_length=50)),
                ('b_fit', models.CharField(max_length=50)),
                ('hair_color', models.CharField(max_length=50)),
                ('skin_color', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_secondary_preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
