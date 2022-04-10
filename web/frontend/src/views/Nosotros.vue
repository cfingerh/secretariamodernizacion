<template>
  <div>
    <section
      class="team"
      v-if="nosotros"
    >
      <div class="container">
        <div class="row justify-content-center">
          <div
            class="col-md-6 col-lg-4"
            v-for="e in primera"
            v-bind:key="e.nombre"
          >
            <div class="team__item">
              <img
                :src="e.cover"
                class="team__img"
              >
              <h3 class="team__title">{{e.nombre}}</h3>
              <h4 class="team__subtitle">{{e.titulo}}</h4>
              <p class="team__description">{{e.descripcion}}</p>
              <a
                :href="e.linkedin"
                class="icon__linkedin"
                target="_blank"
              >
                <font-awesome-icon :icon="['fab', 'linkedin']" />
              </a>
            </div>
          </div>
        </div>
        <div class="row justify-content-center">
          <div
            class="col-md-4"
            v-for="e in segunda"
            v-bind:key="e.nombre"
          >
            <div class="team__item">
              <img
                :src="e.cover"
                class="team__img"
              >
              <h3 class="team__title">{{e.nombre}}</h3>
              <h4 class="team__subtitle">{{e.titulo}}</h4>
              <p class="team__description">{{e.descripcion}}</p>
              <a
                v-if="e.linkedin"
                :href="e.linkedin"
                class="icon__linkedin"
                target="_blank"
              >
                <font-awesome-icon :icon="['fab', 'linkedin']" />
              </a>
            </div>
          </div>
        </div>
        <div class="row  justify-content-center">
          <div
            class="col-md-6 col-lg-4"
            v-for="e in tercera"
            v-bind:key="e.nombre"
          >
            <div class="team__item">
              <img
                v-if="e.cover"
                :src="e.cover"
                class="team__img"
              >
              <h3 class="team__title">{{e.nombre}}</h3>
              <h4 class="team__subtitle">{{e.titulo}}</h4>
              <p class="team__description">{{e.descripcion}}</p>
              <a
                :href="e.linkedin"
                class="icon__linkedin"
                target="_blank"
              >
                <font-awesome-icon :icon="['fab', 'linkedin']" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import axios from 'axios'
export default {
    name: 'Nosotros',
    components: {
    },
    data () {
        return {
            nosotros: [],
            primera: [],
            segunda: [],
            tercera: []
        }
    },
    mounted () {
        var primera = []
        var segunda = []
        var tercera = []
        axios
            .get('./json/nosotros.json')
            .then(response => {
                this.nosotros = response.data.data.nosotros
                this.nosotros.filter(function (item) {
                    if (item.posicion === 1) {
                        primera.push(item)
                    } else if (item.posicion === 2) {
                        segunda.push(item)
                    } else if (item.posicion === 3) {
                        tercera.push(item)
                    }
                })
                this.primera = primera
                this.segunda = segunda
                this.tercera = tercera
            })
            .catch(error => console.log(error))
    }
}
</script>
