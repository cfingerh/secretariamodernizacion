<template>
  <div class="container" style="padding-bottom:150px">
    <div class="content-login">
      <div class="card">
        <div class="card-header bg--dark-blue">
          <h2 class="card-title" v-if="$route.meta.modulo==='bgi'">Bienvenido al Portal de Gestión BGI v0.1</h2>
          <h2 class="card-title" v-if="$route.meta.modulo==='satisfaccion'">Bienvenido al Portal de Encuesta de Satisfacción</h2>
        </div>
        <div class="card-body login">
          <!-- <h3>El portal estará habilitado a partir del martes 17 de noviembre.</h3> -->
          <div class="row">
            <div class="col-12 col-md-6" v-if="loginCU  && !isLoginWithHash">
              <div v-show="loginError" class="alert alert-warning" role="alert">Usted no está registrado. Comuníqueses con su superior encargado</div>
              Ingreso con Clave Única<br>
              <a class="btn-cu" href="#" @click="goToClaveUnica()">
                <span class="cl-claveunica"></span>
                <span class="texto-cu" style="color:white">Iniciar sesión</span>
              </a>
              <hr />
            </div>
            <div v-if="isLoginWithHash">Redireccionando....</div>
            <div class="col-12 col-md-6" vifss="loginOld && !isLoginWithHash">
              Ingreso alternativo para usuarios sin Clave Única
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
                <div v-show="loginError" class="alert alert-warning" role="alert">"Usted no está registrado. Comuníqueses con su superior encargado"</div>
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
import { utils } from '@/utils.js'

export default {
    mixins: [utils],
    name: 'Login',
    components: {},
    data () {
        return {
            isLoginWithHash: false,
            loginError: this.$route.query.error || false,
            loginOld: this.$route.query.method || (process.env.VUE_APP_LOGIN_OLD === 'on') || false,
            loginCU: process.env.VUE_APP_CU !== 'off' || false,
            loginData: { username: null, password: null },
            urlClaveUnica: process.env.VUE_APP_CU,
        }
    },
    mounted () {
        localStorage.removeItem('jwt.access')
        localStorage.removeItem('jwt.refresh')
        this.login_with_hash()
    },

    methods: {
        login_with_hash () {
            var self = this
            var username = self.$route.query.username
            var hash = self.$route.query.hash
            if (!username || !hash) { return }
            self.isLoginWithHash = true
            var url = '/users/login_with_hash/'
            self.loginError = false
            axios({ url: url, params: { username: username, hash: hash }, })
                .then(function (response) {
                    localStorage.setItem('jwt.access', response.data.access)
                    localStorage.setItem('jwt.refresh', response.data.refresh)
                    axios.get('/users/info/').then(function (res) {
                        self.$store.commit('putUser', res.data)
                        self.getServicesAndContinue()
                    })
                })
                .catch(function (response) {
                    self.error = response
                    self.loginError = true
                })
        },
        // getServicesAndContinue () {
        //     var self = this
        //     axios.get('/services').then(function (res) {
        //         self.services = res.data
        //         self.$store.commit('putServices', self.services)

        //         var service = self.services.filter(function (item) {
        //             return item.id === self.$route.params.service * 1
        //         })
        //         if (service.length > 0) {
        //             self.$store.commit('putService', service[0])
        //         } else {
        //             self.$store.commit('putService', self.services[0])
        //         }
        //         self.$router.push({ name: 'Home' })
        //     })
        // },
        goToClaveUnica () {
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
            axios({ method: 'post', url: url, data: { username: self.loginData.username, password: self.loginData.password, }, })
                .then(function (response) {
                    localStorage.setItem('jwt.access', response.data.access)
                    localStorage.setItem('jwt.refresh', response.data.refresh)
                    axios.get('/usuarios/info/').then(function (res) {
                        self.$store.commit('putUser', res.data)
                        self.$router.push({ name: 'Portal' })
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
