<template>
<div>
    <section>
        <div class="container">
            <table class="table">
                <tr>
                    <th>Nombre</th>
                    <th>2015</th>
                    <th>2016</th>
                    <th>2017</th>
                    <th>2018</th>
                    <th>2019</th>
                    <th>2020</th>
                </tr>
                <tr v-for="institucion in instituciones" :key="institucion.codigo">
                    <td>{{institucion.nombre}}</td>
                    <td>{{institucion["2015"]}}</td>
                    <td>{{institucion["2016"]}}</td>
                    <td>{{institucion["2017"]}}</td>
                    <td>{{institucion["2018"]}}</td>
                    <td>{{institucion["2019"]}}</td>
                    <td>{{institucion["2020"]}}</td>
                </tr>
            </table>

        </div>
    </section>
</div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Resumen',
    components: { },
    mixins: [],
    data () {
        return {
            instituciones: []

        }
    },
    methods: {

        getResumen (input) {
            axios.get(process.env.VUE_APP_BASEURL + '/api/resumen').then(res => {
                this.instituciones = res.data
            })
        }
    },
    mounted () {
        this.getResumen()
    }
}
</script>
