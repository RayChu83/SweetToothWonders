# Generated by Django 4.2.5 on 2023-09-16 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Stw_App', '0023_rename_items_cartobject_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedlaterobject',
            name='linked_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
