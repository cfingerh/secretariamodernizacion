<template>
  <footer>
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <img src="/img/logo.png" class="footer__logo">
            </div>
            <div class="col-md-3">
                <p>Teatinos 120, Santiago de Chile<br>
                Fono: +56 2 2828 2000</p>
            </div>
            <div class="col-md-3">
                <ul class="footer__links">
                    <li><a href="/" class="footer__link">Inicio</a></li>
                    <li><a href="/generales" class="footer__link">Resultados Generales</a></li>
                    <li><a href="/resultados" class="footer__link">Resultados por Institución</a></li>
                    <li><a href="/metodologia" class="footer__link">Metodología</a></li>
                </ul>
            </div>
            <div class="col-md-3">
                <p class="float-end"><a href="#">Subir</a></p>
                <ul class="footer__links">
                    <li><a href="/login" class="footer__link">Ingreso Funcionarios</a></li>
                </ul>
            </div>
        </div>
        <img src="/img/gob-line.svg" class="footer__gob-line">
    </div>
  </footer>
</template>
<script>

export default {
    name: 'footer',
    components: {},
    data () {
        return {
            form: null
        }
    }
}
</script>
