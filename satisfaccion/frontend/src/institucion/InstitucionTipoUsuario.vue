<template>
    <div class="ficha">
        <div class="chart__header">
            <h2>Satisfacción última experiencia por tipo de usuario</h2>
            <h4>{{institucion.nombre}}</h4>
        </div>
        <div class="chart__body">
            <div class="row">
                <div class="col-12 col-md-4 ajustado izquierda">
                    <select class="form-control" v-model="config.grupo" @change="cambiar_local()">
                        <option value="edad">Edad</option>
                        <option value="sexo"> Género</option>
                        <option value="educacion">Nivel educacional</option>
                        <option value="habilitado">Habilitación</option>
                    </select>

                    <div v-show="config.periodo==='historico'">
                        Para la vista evolutiva seleccione un rango:
                        <div class="form-check" v-for="opcion in filtros[config.grupo]" v-bind:key="opcion.id">
                            <input class="form-check-input" v-model="filtroSel" type="radio" :value="opcion.id" :name="`grupoUsuario${config.grupo}`" :id="`grupoUsuario${config.grupo}`" @change="cambiar_local()">
                            <label class="form-check-label" for="flexRadioDefault1">
                                {{opcion.nombre}}
                            </label>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-8 ajustado derecha p-4">
                    <h4>Satisfacción última experiencia</h4>
                    <div class="row">
                        <div class="col">
                            <label class="form-check-label" style="float:right" for="radioSatisfaccion">Año 2020</label>
                            <input @change="cambiar_local()" value="ultimo" v-model="config.periodo"  class="form-check-input" style="float:right; margin-right:10px" type="radio" name="radioSatisfaccion" id="radioSatisfaccionUltimo">
                        </div>
                        <div class="col">
                            <input @change="cambiar_local()" value="historico" v-model="config.periodo" class="form-check-input" style="float:left;margin-right:10px" type="radio">
                            <label  class="form-check-label" style="float:left"  for="radioSatisfaccion">Histórico</label>
                        </div>
                    </div>
                    <div v-show="mostrar" id="institucion-tipo-chart">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { utils } from '@/utils.js'

export default {
    name: 'HistoricChart',
    props: ['institucion'],
    mixins: [utils],
    data () {
        return {
            config: {
                elementId: 'institucion-tipo-chart',
                tipo_grafico: 'barra',
                medicion: 'experiencia',
                periodo: 'historico',
                grupo: 'edad',

            },

            filtroSel: 'todos',
            filtros:
                {
                    edad: [
                        { id: 'todos', nombre: 'Todas las edades' },
                        { id: '18_a_34', nombre: '18 a 34 años' },
                        { id: '35_a_44', nombre: '35 a 44 años' },
                        { id: '45_a_54', nombre: '45 a 54 años' },
                        { id: '55_y_mas', nombre: '55 años y más' },
                    ],
                    sexo: [
                        { id: 'todos', nombre: 'Todos' },
                        { id: 'mujer', nombre: 'Mujeres' },
                        { id: 'hombre', nombre: 'Hombres' },
                        { id: 'no_responde', nombre: 'Prefiero no responder' },
                    ],
                    educacion: [
                        { id: 'todos', nombre: 'Todos' },
                        { id: 'Escolar incompleta', nombre: 'Enseñanza Básica' },
                        { id: 'Escolar completa', nombre: 'Enseñanza Media' },
                        { id: 'Superior', nombre: 'Superior' }
                    ],
                    habilitado: [
                        { id: 'todos', nombre: 'Todos' },
                        { id: 'Habilitado', nombre: 'Habilitado' },
                        { id: 'Medianamente habilitado', nombre: 'Medianamente habilitado' },
                        { id: 'No habilitado', nombre: 'No habilitado' }
                    ]
                }
        }
    },
    methods: {

        cambiar_local () {
            if (this.filtros[this.config.grupo].filter(f => { return f.id === this.filtroSel }).length === 0) {
                this.filtroSel = 'todos'
            }
            var filtro = {}
            if (this.config.grupo && this.filtroSel !== 'todos') {
                filtro[this.config.grupo] = this.filtroSel
            }
            this.config.filtro = filtro
            if (this.config.periodo === 'historico') {
                this.config.tipo_grafico = 'barra'
                this.config.filtro.anio = null
            } else {
                this.config.tipo_grafico = 'barra_tipo'
                this.config.filtro = { anio: this.institucion.datos.anios[this.institucion.datos.anios.length - 1] }
            }
            this.cambiar(this.config)
        }

    },
    mounted () {
        this.cambiar_local()
    }
}
</script>
