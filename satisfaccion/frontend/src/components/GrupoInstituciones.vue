<template>
    <div>
        <div class="group-instituciones card card--link">
            <h2 class="group-instituciones__title">{{grupo}}</h2>
            <div class="grupo group-instituciones__item" v-for="institucion in get_grupo(grupo)" v-bind:key="institucion.id" >
                <router-link :to="`/detalleservicio/${institucion.codigo_dipres}/${institucion.codigo}`" class="card__link">{{institucion.nombre}}</router-link>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'DetalleServicio',
    components: {},
    props: ['grupo', 'grupos'],
    mixins: [],
    data () {
        return {
            form: { buscar: null }
        }
    },
    methods: {
        get_grupo: function (nombreGrupo) {
            return this.grupos.filter(g => {
                return g.nombre === nombreGrupo
            })[0].instituciones.filter(i => { return i.nombre })
        },
        buscar: function () {
        }

    },
    mounted () {
    }
}
</script>
