# Generated by Django 5.1.6 on 2025-02-27 17:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_customuser_role_alter_customuser_is_active'),
        ('groupe', '0002_group_academic_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='groups',
            field=models.ManyToManyField(related_name='professors', to='groupe.group'),
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='groupe.group'),
        ),
    ]
