<template>
    <div id="app">
        <Header></Header>
        <Banner></Banner>
        <router-view/>
        <Footer></Footer>
    </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Banner from '@/components/Banner.vue'
import Footer from '@/components/Footer.vue'

export default {
    name: 'App',
    components: {
        Header,
        Banner,
        Footer
    }
}
</script>
