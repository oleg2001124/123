# Generated by Django 4.2.11 on 2024-04-19 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Katigori', 'verbose_name_plural': 'boom'},
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225, verbose_name='GLOBAL')),
                ('short_description', models.TextField(max_length=250, verbose_name='micro text')),
                ('full_description', models.TextField(max_length=250, verbose_name='full text')),
                ('preview', models.ImageField(blank=True, upload_to='articles/', verbose_name='Photo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('views', models.IntegerField(default=0, verbose_name='Setings')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='MY WORK')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category', verbose_name='Integer')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
