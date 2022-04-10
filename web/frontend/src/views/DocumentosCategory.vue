<template>
  <div>
    <section>
      <div class="container" v-if="documento">
        <div class="row">
          <div class="col">
            <nav aria-label="breadcrumb">
              <ol class="breadcrumb">
                <li class="breadcrumb-item">
                  <router-link to="/">Inicio</router-link>
                </li>
                <li class="breadcrumb-item">
                  <router-link to="/documentos">Documentos</router-link>
                </li>
                <li class="breadcrumb-item active" aria-current="page">{{documento.categoria_titulo}}</li>
              </ol>
            </nav>
            <div class="documentos__header">
              <h2 class="documentos__title">{{documento.categoria_titulo}}</h2>
              <div v-html="documento.categoria_descripcion"></div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section>
      <div class="container">
        <div class="row">
          <div class="col">
            <!-- {{documento.titulo}}
                        {{documento.descripcion}} -->

            <!-- históricos -->
            <div class="accordion mb-5" id="accordionDocumentos" v-if="documento && documento.categoria_titulo == 'Históricos'">
              <div class="card" v-for="doc in documento.panel" v-bind:key="doc.id">
                <div class="card-header" :id="doc.id">
                  <h2 class="mb-0">
                    <button class="documentos__btn collapsed" type="button" data-toggle="collapse" :data-target="'#collapse'+doc.id" :aria-expanded="false" :aria-controls="'collapse'+doc.id" @click="setCollapse('collapse'+doc.id)">{{doc.titulo}}
                      <font-awesome-icon :icon="['fas', 'angle-down']" class="documentos__icon" v-if=" collapse!=='collapse'+doc.id" />
                      <font-awesome-icon :icon="['fas', 'angle-up']" class="documentos__icon" v-if=" collapse=='collapse'+doc.id" />
                    </button>
                  </h2>
                </div>
                <div :id="'collapse'+doc.id" class="collapse" :aria-labelledby="doc.id" data-parent="#accordionDocumentos">
                  <div class="card-body" v-for="subtitulo in doc.subtitulos" v-bind:key="subtitulo.id">
                    <img src="/img/icon_documento.svg" class="documentos__icon--sm">
                    <router-link :to="'/documento-single?documento=' + subtitulo.id" class="documentos__more">
                      <h3 class="documentos__subtitulo">{{subtitulo.titulo}}</h3>
                      <small class="documentos__subtitulo-archivos">{{subtitulo.documentos.length}} archivo para descargar</small>
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- diagnósticos-->
        <div class="row" v-if="documento && documento.categoria_titulo !='Históricos' && documento.categoria_titulo !='Seminarios'">
          <div class="col">
            <ul class="documentos__list-item">
              <li class="documentos__item" v-for="doc in documento.subtitulos" v-bind:key="doc.id">
                <img src="/img/icon_documento.svg" class="documentos__icon--sm">
                <router-link class="documentos__more" :to="'/documento-single?documento=' + doc.id" v-if="documento.categoria_titulo != 'Agenda de Modernización'">
                  <h3 class="documentos__subtitulo">{{doc.titulo}}</h3>
                  <small class="documentos__subtitulo-archivos">{{doc.documentos.length}} archivo para descargar</small>
                </router-link>
                <a target="_blank" class="documentos__more" :href="'https://s3-sa-east-1.amazonaws.com/modernizacion.hacienda.cl/'+ doc.documentos[0].ruta_documento + doc.documentos[0].documento" v-if="documento.categoria_titulo == 'Agenda de Modernización'">
                  <h3 class="documentos__subtitulo">{{doc.titulo}}</h3>
                  <small class="documentos__subtitulo-archivos">{{doc.documentos.length}} archivo para descargar</small>
                </a>
              </li>
            </ul>
          </div>
        </div>

        <!--seminarios-->
        <div v-if="documento && documento.categoria_titulo ==='Seminarios'">
          <div class="row mb-5" v-for="doc in documento.subtitulos" v-bind:key="doc.id">
            <div class="col-md-7">
              <h3 class="documento__description-title">{{documento.subtitulos[0].titulo}}</h3>
              <h4 class="documentos__archivos">Descripción :</h4>
              <span v-html="documento.subtitulos[0].descripcion"></span>
              <img :src="documento.subtitulos[0].flyer">
            </div>
            <div class="col-md-5">
              <h3 class="documentos__archivos">Descargar documentos:</h3>
              <ul class="documento__list-item-download" v-if="documento.subtitulos[0].documentos">
                <li class="documento__item-download">
                  <!-- <input type="checkbox" @click="seleccionarTodos()" v-model="allSelected">
                                <span class="documento__item-download-name">Todos</span> -->
                  <label class="container-checkbox">
                    <span class="documento__item-download-name">Todos</span>
                    <input type="checkbox" @click="seleccionarTodos()" v-model="allSelected">
                    <span class="checkmark"></span>
                  </label>
                </li>
                <li class="documento__item-download" v-for="doc in documento.subtitulos[0].documentos" v-bind:key="doc.id">
                  <label class="container-checkbox">
                    <a target="_blank" :href="'https://s3-sa-east-1.amazonaws.com/modernizacion.hacienda.cl/'+ doc.ruta_documento + doc.documento">
                      <span class="documento__item-download-name">
                        <h4 class="documento__item-download-title">{{doc.titulo}}</h4>
                        <p class="documento__item-download-date">{{doc.descripcion}}</p>
                        <small class="documento__item-download-date">{{doc.fecha}}</small>
                      </span>
                    </a>
                    <input type="checkbox" name="" v-model="documentosSeleccionados" :value="doc.ruta_documento + ';' + doc.documento">
                    <span class="checkmark"></span>
                  </label>
                </li>
              </ul>
              <button class="btn btn-primary btn-primary--outline" @click="downloadFiles()" v-if="documentosSeleccionados.length > 0">
                <font-awesome-icon :icon="['fas', 'download']" /> Descargar
              </button>
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
    name: 'DocumentosCategory',
    components: {},
    data () {
        return {
            documento: [],
            params: '',
            documentosSeleccionados: [],
            collapse: null,
            rutas: [],
            allSelected: false
        }
    },
    mounted () {
        var self = this
        self.params = Number(self.$route.query.categoria)
        axios
            .get('./json/documentos_detalle.json')
            .then(response => {
                response.data.data.documentos.filter(function (item) {
                    if (item.categoria_id === self.params) {
                        self.documento.push(item)
                        if (item.subtitulos) {
                            item.subtitulos.filter(function (i) {
                                if (i.documentos) {
                                    i.documentos.filter(function (o) {
                                        self.rutas.push(
                                            o.ruta_documento + ';' + o.documento
                                        )
                                    })
                                }
                            })
                        }
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
                var fileExtension = fileName.split('.')[
                    fileName.split('.').length - 1
                ]
                if (fileExtension === 'pdf') {
                    axios({
                        url:
                            'https://cors-anywhere.herokuapp.com/https://s3-sa-east-1.amazonaws.com/modernizacion.hacienda.cl/' +
                            file,
                        method: 'GET',
                        responseType: 'blob'
                    }).then(response => {
                        var fileURL = window.URL.createObjectURL(
                            new Blob([response.data])
                        )
                        var fileLink = document.createElement('a')

                        fileLink.href = fileURL
                        fileLink.setAttribute('download', fileName)
                        document.body.appendChild(fileLink)

                        fileLink.click()
                    })
                } else {
                    window.open(
                        'https://s3-sa-east-1.amazonaws.com/modernizacion.hacienda.cl/' +
                            file,
                        '_blank'
                    )
                }
            })
        },
        setCollapse: function (collapseId) {
            if (this.collapse === collapseId) {
                this.collapse = null
            } else {
                this.collapse = collapseId
            }
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
