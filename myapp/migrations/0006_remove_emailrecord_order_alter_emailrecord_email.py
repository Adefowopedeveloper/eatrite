# Generated by Django 5.2 on 2025-05-02 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_emailrecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailrecord',
            name='order',
        ),
        migrations.AlterField(
            model_name='emailrecord',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
