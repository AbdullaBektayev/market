# Generated by Django 3.1.5 on 2021-01-08 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0004_auto_20210107_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='link',
            field=models.CharField(max_length=200, verbose_name='Link to shop'),
        ),
    ]
