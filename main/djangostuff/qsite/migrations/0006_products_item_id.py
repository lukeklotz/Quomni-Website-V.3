# Generated by Django 4.2.4 on 2023-08-27 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qsite', '0005_userpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='item_id',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]