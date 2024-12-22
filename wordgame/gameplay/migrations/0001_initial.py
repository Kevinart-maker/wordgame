# Generated by Django 5.0.6 on 2024-10-23 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, unique=True)),
                ('definition', models.TextField()),
                ('difficulty', models.IntegerField(default=1)),
            ],
        ),
    ]
