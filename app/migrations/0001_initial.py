# Generated by Django 5.1.3 on 2024-12-14 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('lang', models.CharField(max_length=10)),
                ('result', models.TextField()),
            ],
        ),
    ]
