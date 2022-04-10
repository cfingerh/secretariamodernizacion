<template>
    <div>
        <sitio-header></sitio-header>
        <main>
            <router-view/>
        </main>
        <sitio-footer></sitio-footer>
    </div>
</template>

<script>
import SitioHeader from '@/components/Header.vue'
import SitioFooter from '@/components/Footer.vue'
export default {
    name: 'App',
    components: {
        SitioHeader,
        SitioFooter
    }
}
</script>
