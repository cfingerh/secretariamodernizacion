# Generated by Django 3.1.2 on 2022-02-14 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_auto_20220214_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuesta',
            name='anio',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
    ]
