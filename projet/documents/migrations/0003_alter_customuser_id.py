# Generated by Django 5.1.6 on 2025-03-14 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
