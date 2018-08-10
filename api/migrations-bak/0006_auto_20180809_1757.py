# Generated by Django 2.1 on 2018-08-09 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180809_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='owner',
            field=models.ForeignKey(default='admin2', on_delete=django.db.models.deletion.CASCADE, related_name='issue', to=settings.AUTH_USER_MODEL),
        ),
    ]