# Generated by Django 3.1.2 on 2021-06-03 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20210601_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEC_eval_presencial',
            new_name='pec_eval_presencial',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEC_eval_telefono',
            new_name='pec_eval_telefono',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEC_eval_web',
            new_name='pec_eval_web',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEV_tram_acogido',
            new_name='pev_tram_acogido',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEV_tram_claridad_pasos',
            new_name='pev_tram_claridad_pasos',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEV_tram_facil',
            new_name='pev_tram_facil',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEV_tram_info_compr',
            new_name='pev_tram_info_compr',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEV_tram_info_util',
            new_name='pev_tram_info_util',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEV_tram_resp_clara',
            new_name='pev_tram_resp_clara',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEV_tram_resp_compl',
            new_name='pev_tram_resp_compl',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEV_tram_resp_util',
            new_name='pev_tram_resp_util',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PEV_tram_tiempo',
            new_name='pev_tram_tiempo',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PI_imagen_actual',
            new_name='pi_imagen_actual',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PI_imagen_funcion',
            new_name='pi_imagen_funcion',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PI_imagen_preocupa',
            new_name='pi_imagen_preocupa',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PI_imagen_satisface',
            new_name='pi_imagen_satisface',
        ),
        migrations.RenameField(
            model_name='respuesta',
            old_name='PI_imagen_transp',
            new_name='pi_imagen_transp',
        ),
    ]
