# Generated by Django 5.0.2 on 2024-02-27 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VNDisplay', '0007_type_android_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='resource',
            field=models.URLField(max_length=250, null=True),
        ),
    ]
