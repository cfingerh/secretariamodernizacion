<template>
    <footer>
        <div class="container bg-blue">
            <div class="row align-items-center justify-content-between">
                <div class="col-md-5">
                    <img class="navbar-brand__img" src="/img/logo_footer.svg">
                    <img src="/img/color-bar.png" class="footer__line">
                </div>
                <div class="col-md-3">
                    <ul class="navbar-nav ml-auto navbar-nav--footer">
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
<!--                         <li class="nav-item">
                            <router-link class="nav-link" to="/destacados">Destacados</router-link>
                        </li> -->
                    </ul>
                </div>
                <div class="col-md-3">
                    <img src="/img/logo_hacienda.svg" class="footer__img">
                    <div class="footer__content">
                        <p class="footer__title">Ministerio de Hacienda</p>
                        <p class="footer__subtitle">Teatinos 120, Santiago de Chile<br>
                        Fono: +56 2 2828 2000</p>
                        <a class="footer__rrss-icon" target="_blank" href="https://twitter.com/ModernizacionMH"><font-awesome-icon :icon="['fab', 'twitter']" /></a>
                        <a class="footer__rrss-icon" target="_blank" href="https://www.linkedin.com/company/secretar%C3%ADa-de-modernizaci%C3%B3n/"><font-awesome-icon :icon="['fab', 'linkedin']" /></a>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</template>
<script>
export default {
    name: 'Header',
    data () {
        return {
            activeClass: 'nav-link-footer--active'
        }
    },
    computed: {
        currentPage () {
            return this.$route.path
        }
    }
}
</script>
