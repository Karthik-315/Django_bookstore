# Generated by Django 3.1.7 on 2021-07-21 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_outlet', '0009_auto_20210721_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AuthoredBooks', to='book_outlet.author'),
        ),
    ]
