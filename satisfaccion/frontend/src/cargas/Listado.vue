7<template>
  <div class="container inicio" >
      <br>
      <br>
      <br>
    <div class="texto">
      <h1>Seleccione una institución</h1>
      <select class="form-select" v-model="institucionSel" v-if="instituciones" @change="load()">
          <option v-for="institucion in instituciones" :key="institucion.id" :value="institucion">{{institucion.nombre}}</option>
      </select>
    </div>

    <div class="texto" v-if="institucionSel && 1===2">
      <h2>Archivos de Datos</h2>
      <hr>
      <b-alert v-if="!is_tipo(['empresa'])" show variant="warning">La empresa encuestadora es la encargada de cargar los archivos</b-alert>

      <table class="table">
        <thead>
          <tr>
            <th colspan="2"></th>
            <th colspan="3" style="text-align:center">Calculados</th>
            <th colspan="3"></th>
          </tr>
          <tr>
            <th>Estado</th>
            <th width="180">Cantidad de Casos</th>
            <th width="180">Evaluación Institución</th>
            <th width="180">Satisfacción Neta</th>
            <th>Descarga Archivo</th>
            <th>Descarga Certificado</th>
            <th colspan="2">Acciones</th>
          </tr>
        </thead>
        <tbody v-if="cargasDatos">
          <tr v-for="carga in cargasDatos" v-bind:key='carga.id'>
            <td>
              <div v-for="log in carga.historial.logs" v-bind:key="log.fechahora">
              {{log.a}} el <b>{{log.fechahora | formatDateTime}}</b>
              </div>
            </td>
            <td v-if="carga.status==='verificado' || carga.status==='aprobado' || carga.status==='rechazado'">{{carga.data.cantidad_registros}}aa</td>
            <td v-if="carga.status==='verificado' || carga.status==='aprobado' || carga.status==='rechazado'">{{carga.data.evaluacion_institucion_porcentaje}} %</td>
            <td v-if="carga.status==='verificado' || carga.status==='aprobado' || carga.status==='rechazado'">{{carga.data.satisfaccion_neta_porcentaje}} %</td>
            <td v-if="carga.status==='no verificado' || carga.status==='subido'" colspan="3"><span v-if="carga.historial.logs.slice(-1)[0].mensajes">{{carga.historial.logs.slice(-1)[0].mensajes.join(" ; ")}}</span></td>

            <td>
              <a :href="carga.data.url" target="_blank">Archivo</a>
            </td>
            <td>
              <span v-if="carga.status==='aprobado'">
                <a :href="linkCertificadoDato(carga)" target="_blank">Certificado</a>
              </span>
            </td>
            <td>
              <b-alert v-if="carga.status==='verificado' && !is_tipo(['administrador'])" show variant="success">Administrador debe Aprobar</b-alert>
              <b-alert v-if="carga.status==='rechazado'" show variant="warning">Rechazado</b-alert>
              <b-alert v-if="carga.status==='aprobado'" show variant="success">Aprobado</b-alert>
              <b-button v-show="carga.status==='verificado' && is_tipo(['administrador'])"
              class="btn btn-success" @click="aprobar(carga)" >Aprobar</b-button>
              <b-button v-show="carga.status==='verificado' && is_tipo(['administrador'])"
              class="btn btn-danger" @click="rechazar(carga)" >Rechazar</b-button>
            </td>
            <td>
               <b-button v-show="carga.status!=='aprobado'" v-if="is_tipo(['empresa', 'administrador'])"
              class="btn btn-warning" @click="eliminar(carga)" >Eliminar</b-button>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- subido->verificado->aprobado / rechazado -->
      <div>
        <form  enctype="multipart/form-data" >
          <input type="file" style="display:none" id="load_datos" :disabled="isSaving || !is_tipo(['empresa'])" @change="filesChange($event.target.files, 'datos')"
            class="input-file">
            <p v-if="isSaving">
              Cargando ....
            </p>
        </form>
         <b-button v-if="is_tipo(['empresa'])" class="btn btn-info" @click="is_clicked('load_datos')" >Agregar archivo</b-button>

      </div>
    </div>

    <div class="texto" v-if="this.cantidad">
      <h2>Resultados</h2>
      Cantidad de registros: {{this.cantidad}} encuestas
      <br>
      Satisfacción última experiencia (neta): {{this.experiencia_neta}} %
      <br>

      Evaluación institución (neta): {{this.eval_inst_neta}} %
      <br>
      <br>
      <a :href="`/2021/${institucionSel.datos.codigo_dipres}.xlsx`">Descargar archivo excel</a>
    </div>

    <div class="texto" v-if="institucionSel && is_tipo(['servicio','administrador'])">
      <h2>Archivos de Presentaciones</h2>
      <hr>
      <!-- <b-alert v-if="!is_tipo(['servicio'])" show variant="warning">El encargado del Servicio es responsable de cargar la presentación</b-alert> -->
      <table class="table">
        <thead>
          <tr>
            <th>Estado</th>
            <th>Archivo</th>
            <th>Descarga Certificado</th>
            <th colspan="2">Acciones</th>
          </tr>
        </thead>
        <tbody v-if="cargasPresentacion">
          <tr v-for="carga in cargasPresentacion" v-bind:key='carga.id'>
            <td>
              <div v-for="log in carga.historial.logs" v-bind:key="log.fechahora">
              {{log.a}} el <b>{{log.fechahora}}</b>
              </div>
            </td>
            <td>
              <span v-if="cargasPresentacion">
                <a :href="cambiarUrl(cargasPresentacion[0].data.url)">Presentación</a>
              </span>
            </td>

            <td>
              <span v-if="carga.status==='aprobado'">
                <a :href="linkCertificadoPresentacion(carga)" target="_blank">Certificado</a>
              </span>
            </td>
            <td>
              <b-alert v-if="carga.status==='subido' && !is_tipo(['administrador'])" show variant="success">Administrador debe Aprobar</b-alert>
              <b-alert v-if="carga.status==='rechazado'" show variant="warning">Rechazado</b-alert>
              <b-alert v-if="carga.status==='aprobado'" show variant="success">Aprobado</b-alert>
              <b-button v-show="carga.status==='subido' && is_tipo(['administrador'])"
              class="btn btn-success" @click="aprobar(carga)" >Aprobar</b-button>
              <b-button v-show="carga.status==='subido' && is_tipo(['administrador'])"
              class="btn btn-danger" @click="rechazar(carga)" >Rechazar</b-button>
            </td>
            <td>
               <b-button v-show="carga.status!=='aprobado'" v-if="is_tipo(['servicio', 'administrador'])"
              class="btn btn-warning" @click="eliminar(carga)" >Eliminar</b-button>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- subido->aprobado / rechazado -->
      <div>
        <form  enctype="multipart/form-data" >
          <input type="file" style="display:none" id="load_presentacion" :disabled="isSaving || !is_tipo(['servicio'])" @change="filesChange($event.target.files, 'presentacion')"
            class="input-file">
            <p v-if="isSaving">
              Cargando ....
            </p>
        </form>
         <b-button v-if="is_tipo(['servicio'])" class="btn btn-info" @click="is_clicked('load_presentacion')" >Agregar archivo</b-button>
      </div>
      </div>

  </div>
</template>

<script>
import axios from 'axios'

import { utils } from '@/utils.js'

export default {
    name: 'Inicio',
    mixins: [utils],
    components: {},
    props: {},
    data () {
        return {
            instituciones: null,
            institucionSel: null,
            isSaving: null,
            cargasDatos: [],
            cargasPresentacion: [],
            experiencia_neta: null,
            eval_inst_neta: null,
            cantidad: null
        }
    },
    methods: {
        cambiarUrl (url) {
            url = url.replace('None', 'satisfaccion2021-web-archivos')
            url = url.replace('s3-satisfaccion2021-web', 'satisfaccion2021-web')
            url = url.replace('amazonaws.com/satisfaccion2021-web-archivos', '')
            url = url.replace('archivos.', 'archivos.s3.sa-east-1.amazonaws.com')
            console.log(url)
            return url
        },
        is_clicked (id) {
            document.getElementById(id).click()
        },
        load_instituciones () {
            axios.get('/portal/instituciones').then(res => {
                this.instituciones = res.data
                if (res.data.length === 1) {
                    this.institucionSel = res.data[0]
                    this.load()
                }
            })
        },

        is_tipo (posibles) {
            var valor = false
            posibles.forEach(posible => {
                if (this.institucionSel.tipos_permisos.indexOf(posible) >= 0) {
                    valor = true
                }
            })
            return valor
        },
        linkCertificadoPresentacion (carga) {
            return (`https://8bl8xgahz9.execute-api.sa-east-1.amazonaws.com/prod/portal/carga/pdf_presentacion/${carga.id}/`)
        },
        linkCertificadoDato (carga) {
            return (`https://8bl8xgahz9.execute-api.sa-east-1.amazonaws.com/prod/portal/carga/pdf_dato/${carga.id}/`)
        },
        aprobar (carga) {
            var self = this
            axios.post(`/portal/cargas/${carga.id}/aprobar/`, { }).then(function (res) { self.load() })
        },
        eliminar (carga) {
            var self = this
            axios.post(`/portal/cargas/${carga.id}/eliminar/`, { }).then(function (res) { self.load() })
        },
        rechazar (carga) {
            var self = this
            axios.post(`/portal/cargas/${carga.id}/rechazar/`, { }).then(function (res) { self.load() })
        },
        load () {
            var form = { institucion: this.institucionSel.id }
            axios.get('/portal/cargas', { params: form }).then(res => {
                this.cargasPresentacion = res.data.filter(function (i) { return i.data.tipo === 'presentacion' })
                this.cargasDatos = res.data.filter(function (i) { return i.data.tipo === 'datos' })
            })

            axios.get(`https://portal.satisfaccion.gob.cl/2021/${this.institucionSel.datos.codigo_dipres}.json`).then(res => {
                this.cantidad = res.data.cantidad
                this.experiencia_neta = Math.round(res.data.experiencia_positivo / res.data.experiencia_total * 100) - Math.round(res.data.experiencia_negativo / res.data.experiencia_total * 100)
                this.eval_inst_neta = Math.round(res.data.eval_inst_positivo / res.data.eval_inst_total * 100) - Math.round(res.data.eval_inst_negativo / res.data.eval_inst_total * 100)
            })

            axios.get(`https://satisfaccion.gob.cl/2021/${this.institucionSel.datos.codigo_dipres}.json`).then(res => {
                this.cantidad = res.data.cantidad
                this.experiencia_neta = Math.round(res.data.experiencia_positivo / res.data.experiencia_total * 100) - Math.round(res.data.experiencia_negativo / res.data.experiencia_total * 100)
                this.eval_inst_neta = Math.round(res.data.eval_inst_positivo / res.data.eval_inst_total * 100) - Math.round(res.data.eval_inst_negativo / res.data.eval_inst_total * 100)
            })

            axios.get(`https://www.satisfaccion.gob.cl/2021/${this.institucionSel.datos.codigo_dipres}.json`).then(res => {
                this.cantidad = res.data.cantidad
                this.experiencia_neta = Math.round(res.data.experiencia_positivo / res.data.experiencia_total * 100) - Math.round(res.data.experiencia_negativo / res.data.experiencia_total * 100)
                this.eval_inst_neta = Math.round(res.data.eval_inst_positivo / res.data.eval_inst_total * 100) - Math.round(res.data.eval_inst_negativo / res.data.eval_inst_total * 100)
            })

            // axios.get(`http://localhost:8080/2021/${this.institucionSel.datos.codigo_dipres}.json`).then(res => {
            //     this.cantidad = res.data.cantidad
            //     this.experiencia_neta = Math.round(res.data.experiencia_positivo / res.data.experiencia_total * 100) - Math.round(res.data.experiencia_negativo / res.data.experiencia_total * 100)
            //     this.eval_inst_neta = Math.round(res.data.eval_inst_positivo / res.data.eval_inst_total * 100) - Math.round(res.data.eval_inst_negativo / res.data.eval_inst_total * 100)
            // })
        },
        getMensajeError (carga) {
            debugger
        },
        // isAprobado (carga) {
        //   return carga.historial.logs.filter(function (i) { return i.s === 'aprobado' }).length > 0
        // },
        save (formData, tipo) {
            var self = this
            this.isSaving = true
            this.upload(formData, tipo).then(x => { self.isSaving = false; self.load() })
        },
        filesChange (fileList, tipo) {
            const formData = new FormData()
            if (!fileList.length) return
            Array.from(Array(fileList.length).keys()).map(x => { formData.append('archivo', fileList[x], fileList[x].name) })
            this.save(formData, tipo)
        },
        upload (formData, tipo) {
            const url = `/portal/subir/${this.institucionSel.id}/?tipo=${tipo}`
            return axios.post(url, formData).then(x => x.data)
        }

    },
    mounted () {
        this.load_instituciones()
    }
}
</script>

<style scoped>

.texto{
  box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
  padding:20px;
  margin:20px;
  background-color: rgb(242, 242, 242);
}

hr {
    height: 8px;
    /* background-color: red; */
    background-image: linear-gradient(90deg, red, transparent);
    border: 0;
    height: 3px;
}

</style>
