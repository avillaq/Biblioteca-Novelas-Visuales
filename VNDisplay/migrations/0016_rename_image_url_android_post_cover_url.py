# Generated by Django 5.0.2 on 2025-01-22 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VNDisplay', '0015_alter_android_post_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='android_post',
            old_name='image_url',
            new_name='cover_url',
        ),
    ]