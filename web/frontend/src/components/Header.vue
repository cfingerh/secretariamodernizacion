<template>
  <nav class="navbar navbar-expand-lg">
  <div class="container">
    <router-link class="navbar-brand" to="/">
      <img class="navbar-brand__img" src="/img/logo.svg">
    </router-link>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <font-awesome-icon :icon="['fas', 'bars']" />
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ml-auto">
        <li class="nav-item">
          <router-link :class="[currentPage === '/' ? activeClass: '', 'nav-link']" to="/">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link :class="[currentPage === '/nosotros' ? activeClass: '', 'nav-link']" to="/nosotros">Nosotros</router-link>
        </li>
        <li class="nav-item">
          <router-link :class="[currentPage === '/proyectos' || currentPage === '/proyecto-single' ? activeClass: '', 'nav-link']" to="/proyectos">Proyectos</router-link>
        </li>
        <li class="nav-item">
            <router-link :class="[currentPage === '/procesos' || currentPage === '/proceso-single' ? activeClass: '', 'nav-link']" to="/procesos">Procesos</router-link>
        </li>
        <li class="nav-item">
          <router-link :class="[currentPage === '/documentos' || currentPage === '/documentos-category' || currentPage === '/documento-single' || currentPage === '/resultados' ? activeClass: '', 'nav-link']" to="/documentos">Documentos</router-link>
        </li>
<!--         <li class="nav-item">
          <router-link class="nav-link" to="/destacados">Destacados</router-link>
        </li> -->
      </ul>
    </div>
    </div>
  </nav>
</template>
<script>
export default {
    name: 'Header',
    data () {
        return {
            activeClass: 'nav-link--active'
        }
    },
    computed: {
        currentPage () {
            return this.$route.path
        }
    }
}
</script>
