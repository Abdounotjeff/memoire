# Generated by Django 5.1.6 on 2025-03-15 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='link',
            field=models.TextField(help_text='recommand using Google meet'),
        ),
    ]
