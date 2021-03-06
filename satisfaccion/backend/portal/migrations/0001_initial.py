# Generated by Django 3.1.2 on 2021-11-03 21:48

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0012_institucion_resumen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('historial', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('institucion', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cargas', to='base.institucion')),
            ],
        ),
    ]
