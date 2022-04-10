<template>
  <div class="container">
    Autenticando
  </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'ClaveUnica',
    components: {},
    data () {
        return {

        }
    },
    mounted () {
        this.login()
    },
    methods: {
        getServicesAndContinue () {
            var self = this
            axios.get('/services').then(function (res) {
                self.services = res.data
                self.$store.commit('putServices', self.services)

                var service = self.services.filter(function (item) {
                    return item.id === self.$route.params.service * 1
                })
                if (service.length > 0) {
                    self.$store.commit('putService', service[0])
                } else {
                    self.$store.commit('putService', self.services[0])
                }
                self.$router.push({ name: 'Home' })
            })
        },
        login () {
            var self = this
            var params = this.$route.query
            console.log(localStorage.getItem('cu_state'))
            console.log(params.state)
            var url = '/usuarios/claveunica/'
            axios({ method: 'post', url: url, data: params })
                .then(function (response) {
                    localStorage.setItem('jwt.access', response.data.access)
                    localStorage.setItem('jwt.refresh', response.data.refresh)
                    self.$router.push({ name: 'cargasListado' })
                })
                .catch(function (response) {
                    window.location = '/login?error=true'
                })
        },

    }
}
</script>
