# Generated by Django 5.1.2 on 2025-02-19 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_alter_appointemt_time'),
        ('doctor', '0002_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointemt',
            name='time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.available_time'),
        ),
    ]
