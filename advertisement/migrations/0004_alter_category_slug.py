# Generated by Django 3.2 on 2021-06-23 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0003_alter_category_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, verbose_name='slug'),
        ),
    ]
