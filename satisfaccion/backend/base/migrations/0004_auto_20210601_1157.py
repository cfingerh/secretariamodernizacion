# Generated by Django 3.1.2 on 2021-06-01 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_respuesta_educacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='PEV_tram_acogido',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PEV_tram_claridad_pasos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PEV_tram_facil',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PEV_tram_info_compr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PEV_tram_info_util',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PEV_tram_resp_clara',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PEV_tram_resp_compl',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PEV_tram_resp_util',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PEV_tram_tiempo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PI_imagen_actual',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PI_imagen_funcion',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PI_imagen_preocupa',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PI_imagen_satisface',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respuesta',
            name='PI_imagen_transp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]