# Generated by Django 5.2 on 2025-05-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_remove_order_items_alter_order_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
