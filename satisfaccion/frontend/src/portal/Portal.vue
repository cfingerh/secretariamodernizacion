<template>
    <div class="container inicio">

        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item breadcrumb-last" aria-current="page">Inicio</li>
            </ol>
        </nav>
        <h2>Bienvenido, {{$store.state.user.nombre_completo}}</h2>
        <div class="texto">
            El Balance de Gestión Integral (BGI) tiene como propósito informar acerca
            de los objetivos, metas y resultados de la gestión de los servicios en
            forma de cuenta pública al Congreso Nacional.
        </div>
        <br>
        <br>
        <h3>Resumen - Estado de Avance de los Servicios</h3>
        <div class="texto">
            <estado-avance></estado-avance>
        </div>
    </div>
</template>

<script>
// import EstadoAvance from '@/components/EstadoAvancesComponent.vue'
import { utils } from '@/utils.js'

export default {
    name: 'Home',
    mixins: [utils],
    components: { // EstadoAvance
    },
    props: {},
    data () {
        return {}
    },
    methods: {},
    mounted () {
    }
}
</script>
