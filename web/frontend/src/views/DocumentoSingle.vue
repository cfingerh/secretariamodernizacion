<template>
    <div>
        <section class="documento mb-5">
            <div class="container" v-if="documento">
                <div class="row">
                    <div class="col">
                        <nav aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item"><router-link to="/">Inicio</router-link></li>
                                <li class="breadcrumb-item"><router-link to="/documentos">Documentos</router-link></li>
                                <li class="breadcrumb-item"><router-link :to="'/documentos-category?categoria=' + documento.categoria_id">{{documento.categoria_titulo}}</router-link></li>
                                <li class="breadcrumb-item" v-if="documento.categoria_titulo == 'Históricos'"><router-link :to="'/documentos-category?categoria=' + documento.categoria_id">{{documento.panel_titulo}}</router-link></li>
                                <li class="breadcrumb-item active" aria-current="page" v-if="documento.documentos">{{documento.documentos.titulo}}</li>
                            </ol>
                        </nav>
                        <div class="documentos__header">
                            <h2 class="documentos__title documentos__title--single mb-3" v-if="documento.documentos">{{documento.documentos.titulo}}</h2>
                            <h3 class="documentos__archivos">Descargar documentos:</h3>
                        </div>
                        <div class="row" v-if="documento.documentos">
                            <div class="col">
                                <ul class="documento__list-item-download" v-if="documento.documentos.documentos">
                                    <li class="documento__item-download">
                                        <!-- <input type="checkbox" @click="seleccionarTodos()" v-model="allSelected">
                                        <span class="documento__item-download-name">Todos</span> -->
                                        <label class="container-checkbox">
                                            <span class="documento__item-download-name">Todos</span>
                                            <input type="checkbox" @click="seleccionarTodos()" v-model="allSelected">
                                            <span class="checkmark"></span>
                                        </label>
                                    </li>
                                    <li class="documento__item-download" v-for="doc in documento.documentos.documentos" v-bind:key="doc.id">
                                        <!-- <input type="checkbox" name="" v-model="documentosSeleccionados" :value="doc.ruta_documento + ';' + doc.documento">
                                        <a target="_blank" :href="'https://s3-sa-east-1.amazonaws.com/modernizacion.hacienda.cl/'+ doc.ruta_documento + doc.documento">
                                            <span class="documento__item-download-name">
                                                <h4 class="documento__item-download-title">{{doc.titulo}}</h4>
                                                <p class="documento__item-download-description">{{doc.descripcion}}</p>
                                                <small class="documento__item-download-date">{{doc.fecha}}</small>
                                            </span>
                                        </a> -->
                                        <label class="container-checkbox">
                                            <a target="_blank" :href="'https://s3-sa-east-1.amazonaws.com/modernizacion.hacienda.cl/'+ doc.ruta_documento + doc.documento">
                                                <span class="documento__item-download-name">
                                                    <h4 class="documento__item-download-title">{{doc.titulo}}</h4>
                                                    <p class="documento__item-download-description">{{doc.descripcion}}</p>
                                                    <small class="documento__item-download-date">{{doc.fecha}}</small>
                                                </span>
                                            </a>
                                            <input type="checkbox" name="" v-model="documentosSeleccionados" :value="doc.ruta_documento + ';' + doc.documento">
                                            <span class="checkmark"></span>
                                        </label>
                                    </li>
                                </ul>
                                <button class="btn btn-primary btn-primary--outline" @click="downloadFiles()" v-if="documentosSeleccionados.length > 0"><font-awesome-icon :icon="['fas', 'download']" /> Descargar</button>
                            </div>
                        </div>
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
    name: 'DocumentoSingle',
    components: {
    },
    data () {
        return {
            documento: [],
            params: '',
            documentosSeleccionados: [],
            rutas: [],
            allSelected: false
        }
    },
    mounted () {
        var self = this
        var detalle = {}
        self.params = self.$route.query.documento
        axios
            .get('./json/documentos_detalle.json')
            .then(response => {
                response.data.data.documentos.filter(function (item) {
                    if (item.subtitulos) {
                        item.subtitulos.filter(function (i) {
                            if (i.id.toString() === self.params) {
                                detalle.categoria_titulo = item.categoria_titulo
                                detalle.categoria_id = item.categoria_id
                                detalle.documentos = i
                                self.documento.push(detalle)
                                i.documentos.filter(function (o) {
                                    self.rutas.push(o.ruta_documento + ';' + o.documento)
                                })
                            }
                        })
                    } else if (item.panel) {
                        item.panel.filter(function (i) {
                            i.subtitulos.filter(function (u) {
                                if (u.id.toString() === self.params) {
                                    detalle.categoria_titulo = item.categoria_titulo
                                    detalle.categoria_id = item.categoria_id
                                    detalle.documentos = u
                                    detalle.panel_titulo = i.titulo
                                    self.documento.push(detalle)
                                    u.documentos.filter(function (o) {
                                        self.rutas.push(o.ruta_documento + ';' + o.documento)
                                    })
                                }
                            })
                        })
                    }
                })
                self.documento = self.documento[0]
            })
            .catch(error => console.log(error))
    },
    methods: {
        downloadFiles: function () {
            $.each(this.documentosSeleccionados, function (key, value) {
                var file = value.split(';')[0] + value.split(';')[1]
                var fileName = value.split(';')[1]
                var fileExtension = fileName.split('.')[fileName.split('.').length - 1]
                if (fileExtension === 'pdf') {
                    axios({
                        url: 'https://cors-anywhere.herokuapp.com/https://s3-sa-east-1.amazonaws.com/modernizacion.hacienda.cl/' + file,
                        method: 'GET',
                        responseType: 'blob'
                    }).then((response) => {
                        var fileURL = window.URL.createObjectURL(new Blob([response.data]))
                        var fileLink = document.createElement('a')

                        fileLink.href = fileURL
                        fileLink.setAttribute('download', fileName)
                        document.body.appendChild(fileLink)

                        fileLink.click()
                    })
                } else {
                    window.open('https://s3-sa-east-1.amazonaws.com/modernizacion.hacienda.cl/' + file, '_blank')
                }
            })
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
        // select: function () {
        //     var self = this
        //     console.log(self.documentosSeleccionados)
        //     console.log(self.rutas.length)¿
        //     if (self.documentosSeleccionados.length === self.rutas.length) {
        //         self.allSelected = true
        //     } else {
        //         self.allSelected = false
        //     }
        // }
    }
}
</script>
