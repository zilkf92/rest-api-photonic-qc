# Generated by Django 2.2 on 2021-05-29 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0018_auto_20210529_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlequbitgate',
            name='params',
            field=models.TextField(null=True),
        ),
    ]
