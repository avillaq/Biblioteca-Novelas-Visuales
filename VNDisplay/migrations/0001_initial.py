# Generated by Django 5.0.2 on 2025-01-23 02:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('resource', models.URLField(max_length=250, null=True)),
            ],
            options={
                'db_table': 'type',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_post', models.CharField(blank=True, max_length=250, unique=True)),
                ('title', models.CharField(max_length=250)),
                ('full_url', models.URLField(max_length=250)),
                ('synopsis', models.TextField()),
                ('cover_url', models.URLField(max_length=300)),
                ('screenshot_urls', models.TextField(blank=True)),
                ('specifications', models.TextField(blank=True)),
                ('publication_date', models.DateField()),
                ('update_date', models.DateField()),
                ('categories', models.ManyToManyField(to='VNDisplay.category')),
            ],
            options={
                'db_table': 'post',
            },
        ),
        migrations.CreateModel(
            name='Android_Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('full_url', models.URLField(max_length=250)),
                ('cover_url', models.URLField(max_length=300)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VNDisplay.type')),
            ],
            options={
                'db_table': 'android_post',
            },
        ),
    ]
