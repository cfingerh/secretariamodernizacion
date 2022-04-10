<template>
    <div>
        <section class="mb-5">
            <div class="container">
                <div class="row">
                    <div class="col" v-if="resultados">
                        <nav aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item"><router-link to="/">Inicio</router-link></li>
                                <li class="breadcrumb-item"><router-link to="/documentos">Documentos</router-link></li>
                                <li class="breadcrumb-item active" aria-current="page">Resultados de búsqueda</li>
                            </ol>
                        </nav>
                        <h3 class="documento__title-resultados">Resultados de búsqueda</h3>
                        <h3 class="documentos__archivos" v-if="resultados.length>0">Descargar documentos:</h3>
                        <ul class="documento__list-item-download" v-if="resultados.length>0">
                            <li class="documento__item-download">
                                <!-- <input type="checkbox" @click="seleccionarTodos()" v-model="allSelected">
                                <span class="documento__item-download-name">Todos</span> -->
                                <label class="container-checkbox">
                                    <span class="documento__item-download-name">Todos</span>
                                    <input type="checkbox" @click="seleccionarTodos()" v-model="allSelected">
                                    <span class="checkmark"></span>
                                </label>
                            </li>
                            <li class="documento__item-download" v-for="doc in resultados" v-bind:key="doc.documento">
                                <!-- <input type="checkbox" name="" v-model="documentosSeleccionados" :value="doc.ruta_documento + ';' + doc.documento"> -->
                                <label class="container-checkbox">
                                    <a target="_blank" :href="'https://modernizacion-hacienda.s3-sa-east-1.amazonaws.com/'+ doc.ruta_documento + doc.documento">
                                        <span class="documento__item-download-name">{{doc.titulo}}</span>
                                    </a>
                                    <input type="checkbox" name="" v-model="documentosSeleccionados" :value="doc.ruta_documento + ';' + doc.documento">
                                    <span class="checkmark"></span>
                                </label>
                            </li>
                        </ul>
                        <button class="btn btn-primary btn-primary--outline" @click="downloadFiles()" v-if="documentosSeleccionados.length > 0"><font-awesome-icon :icon="['fas', 'download']" /> Descargar</button>
                        <span v-if="resultados.length==0">
                            No existen documentos
                        </span>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>
<script>
import axios from 'axios'
import $ from 'jquery'

export default {
    name: 'Resultados',
    components: {
    },
    data () {
        return {
            resultados: [],
            params: '',
            documento: [],
            documentosSeleccionados: [],
            rutas: [],
            allSelected: false
        }
    },
    mounted () {
        var self = this
        self.params = self.$route.query.busqueda
        axios
            .get('./json/documentos.json')
            .then(response => {
                response.data.data.documentos.filter(function (item) {
                    if (item.titulo.toLowerCase().includes(self.params.toLowerCase())) {
                        self.resultados.push(item)
                        self.rutas.push('https://modernizacion-hacienda.s3-sa-east-1.amazonaws.com/' + item.documento)
                    }
                })
            })
            .catch(error => console.log(error))
    },
    methods: {
        downloadFiles: function () {
            $.each(this.documentosSeleccionados, function (key, value) {
                var file = value.split(';')[0] + value.split(';')[1]
                window.open('https://modernizacion-hacienda.s3-sa-east-1.amazonaws.com/' + file, '_blank')
            })
            // axios
            //     .get(process.env.VUE_APP_BASEURL + '/base/download_files/', { params: this.documentosSeleccionados, responseType: 'arraybuffer' })
            //     .then(response => {
            //         console.log(response)
            //         var fileURL = window.URL.createObjectURL(new Blob([response.data]))
            //         var fileLink = document.createElement('a')

            //         fileLink.href = fileURL
            //         fileLink.setAttribute('download', 'Resultados.zip')
            //         document.body.appendChild(fileLink)

            //         fileLink.click()
            //     })
            //     .catch(error => console.log(error))
        },
        seleccionarTodos: function () {
            var self = this
            self.allSelected = true
            if (self.documentosSeleccionados.length === self.rutas.length) {
                self.documentosSeleccionados = []
            } else {
                self.rutas.filter(function (r) {
                    self.documentosSeleccionados.push(r)
                })
            }
        }
    }
}
</script>
