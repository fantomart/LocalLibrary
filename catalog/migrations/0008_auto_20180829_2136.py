# Generated by Django 2.1 on 2018-08-29 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20180829_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='img',
            field=models.ImageField(blank=True, upload_to='catalog/static/media/images/'),
        ),
    ]
