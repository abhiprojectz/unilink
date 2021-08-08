# Generated by Django 3.2.4 on 2021-07-31 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UniCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('collection_name', models.CharField(max_length=300, null=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('short_url', models.CharField(blank=True, max_length=15, unique=True)),
            ],
            options={
                'db_table': 'unicollection',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=300, null=True)),
                ('image_url', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('url', models.URLField()),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='unilink_app.unicollection')),
            ],
            options={
                'db_table': 'links',
                'ordering': ['-created'],
            },
        ),
    ]