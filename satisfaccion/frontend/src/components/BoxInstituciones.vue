<template>
  <div class="box-instituciones card card--link" v-if="institucion" style="max-height:460px">
    <div class="box-instituciones__header">
        <div class="row">
            <div class="col-md-4">
                <img :src="get_logo(institucion)" style="max-width:100%;max-height:70px">
            </div>
            <div class="col-md-8">
                <h3 class="box-instituciones__title card__title">
                    <a :href="'/detalleservicio/'+institucion.datos.codigo_dipres+'/'+institucion.datos.codigo">{{institucion.nombre_a_mostrar}}</a>
                </h3>
                <h4 class="box-instituciones__percent box-instituciones__percent--lg">{{institucion.datos.satisfaction_neta}} % usuarios satisfechos</h4>
                <!-- <small class="box-instituciones__percent-text">Satisfaccion Neta</small> -->
                <!-- <small class="d-block">Índice de Satisfacción Positiva última experiencia</small> -->
            </div>
        </div>
    </div>
    <div class="box-instituciones__container-chart">
      <div class="row">
        <div class="col-12" v-if="institucion && institucion.datos.anios && institucion.datos.anios.length>1">
            <small>Tendencia por año</small>
            <historic-chart :institucion='institucion'></historic-chart>
            <p class="text-center esconder-chico">Revisar la <a :href="'/detalleservicio/'+institucion.datos.codigo_dipres+'/'+institucion.datos.codigo">Ficha de la Institución</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import HistoricChart from './HistoricChart.vue'

export default {
    name: 'BoxInstituciones',
    components: { HistoricChart },
    props: ['institucion'],
    data () {
        return {
            datacollection: null,
            chartOptions: null
        }
    },
    methods: {
        heightSatisfaction: function (height) {
            return {
                height: `${height}px`
            }
        },
        get_logo (institucion) {
            if (institucion.datos.codigo.toLowerCase().search('serviu') >= 0) {
                return '/img/logos/serviu.png'
            }
            if (institucion.datos.codigo.toLowerCase().search('chilecompra') >= 0) {
                return '/img/logos/chilecompra.png'
            }
            if (institucion.datos.codigo.toLowerCase().search('chileatiende') >= 0) {
                return '/img/logos/chileatiende.png'
            }
            if (institucion.datos.codigo.toLowerCase().search('chileaatiende') >= 0) {
                return '/img/logos/chileatiende.png'
            }
            return `/img/logos/${institucion.datos.codigo.toLowerCase()}.png`
        }

    },
    mounted () {

    }

}
</script>
