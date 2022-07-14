<template>
  <div class="container" style="padding-bottom:150px">
    <div class="content-login">
      <div class="card">
        <div class="card-header bg--dark-blue">
          <h2 class="card-title">Bienvenido al Portal de Gestión BGI</h2>
        </div>
        <div class="card-body login">
          <div class="row">
            <div class="col-12 col-md-6">
              <div class="form">
                <div class="form-group">
                  <label>Usuario</label>
                  <input type="text" class="form-control" v-model="loginData.username" placeholder="Usuario" />
                  <small class="form-text text-muted"></small>
                </div>
                <div class="form-group">
                  <label>Clave</label>
                  <input type="password" class="form-control" v-model="loginData.password" placeholder="Clave" />
                  <small class="form-text text-muted"></small>
                </div>
                <br />
                <div v-show="loginError" class="alert alert-warning" role="alert">Credenciales incorrectas</div>
                <button type="button" class="btn btn-primary" @click="loginFuncionario">Ingresar</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  components: {},
  data () {
    return {
      loginError: this.$route.query.error || false,
      loginData: { username: null, password: null },
      urlClaveUnica: process.env.VUE_APP_CU,
    }
  },
  mounted () {
    localStorage.removeItem('jwt.access')
    localStorage.removeItem('jwt.refresh')
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
    goToClaveUnica () {
      // window.location = '/'
      // var clientId = '3Dcb2719c46dc54f3fa01a56a00d6f71fe'
      var state = this.makeState(30)
      localStorage.setItem('cu_state', state)

      var url = `${this.urlClaveUnica}${state}`
      window.location = url
    },

    makeState (length) {
      var result = ''
      var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
      var charactersLength = characters.length
      for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength))
      }
      return result
    },

    loginFuncionario (e) {
      var self = this
      e.preventDefault()
      var url = '/api/token/'
      self.loginError = false
      axios({
        method: 'post',
        url: url,
        data: {
          username: self.loginData.username,
          password: self.loginData.password,
        },
      })
        .then(function (response) {
          localStorage.setItem('jwt.access', response.data.access)
          localStorage.setItem('jwt.refresh', response.data.refresh)
          axios.get('/users/info/').then(function (res) {
            // debugger
            self.$store.commit('putUser', res.data)
            self.getServicesAndContinue()
          })
        })
        .catch(function (response) {
          self.error = response
          self.loginError = true
        })
    },
  },
}
</script>
