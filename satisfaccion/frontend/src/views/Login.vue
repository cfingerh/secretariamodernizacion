<template>
    <div>
        <div class="container">
          <div style="padding:40px">
            Esta página es sólo para funcionarios de las instituciones participantes.
            <br>
              <a style="" class="btn-cu btn-m  btn-color-estandar" title="Este es el botón Iniciar sesión de ClaveÚnica" :href="urlClaveUnica">
                  <span class="cl-claveunica"></span>
                  <span class="texto">Iniciar sesión</span>
              </a>
          </div>
          <hr>
          <!-- <div style="padding:40px">
              En esta sección, las empresas pueden validar su archivo de datos
              <br>
            <button class="button--sm button--pill button-line--warning" @click="onPickFile()">Adjuntar</button>
            <input type="file" style="display: none" ref="fileInput" accept="image/*" @change="onFilePicked"/>
            </div> -->
        </div>
        <!-- <div class="row justify-content-center py-5">
          <form id="loginContent" class="my-5">
                <h3>Autenticación de Usuario</h3>
                <small>Acceso habilitado sólo durante testing</small>
                <input type="text" id="login" class="fadeIn second login__input" name="login" placeholder="usuario" v-model="loginData.username">
                <input type="password" id="password" class="fadeIn third login__input" name="login" placeholder="clave" v-model="loginData.password">
                <button class="mt-1 btn btn-pill-primary" type="button" @click="loginFuncionario">Ingresar</button>
            </form>
        </div> -->
    </div>
    </template>
<script>

import axios from 'axios'
export default {
    data () {
        return {
            urlClaveUnica: null,
            mensajes: null,
            data: null,
            loginData: {}
        }
    },
    methods: {
        onPickFile () {
            this.$refs.fileInput.click()
        },
        onFilePicked (event) {
            const files = event.target.files
            const fileReader = new FileReader()
            fileReader.addEventListener('load', () => { this.imageUrl = fileReader.result })
            fileReader.readAsDataURL(files[0])
            this.image = files[0]
            const formData = new FormData()

            formData.append('archivo', this.image)

            var url = '/portal/subir/0/'
            axios.post(url, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            ).then(res => {
                this.mensajes = res.data.mensajes
                this.data = res.data.data
            })
        },

        // loginClaveUnica: async function() {
        //   try {
        //     const res = await axios.get(
        //       ``
        //     );
        //     console.log(res);
        //   } catch (error) {
        //     console.log(error);
        //   }
        // },
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
            e.preventDefault()
            var url = '/api/token/'
            var self = this
            self.loginError = false
            axios({
                method: 'post',
                url: url,
                data: {
                    username: this.loginData.username,
                    password: this.loginData.password,
                },
            }).then((resp) => {
                localStorage.setItem('jwt.access', resp.data.access)
                localStorage.setItem('jwt.refresh', resp.data.refresh)
                this.$router.push({ name: 'cargasListado' })
            }).catch(function (response) {
                self.error = response
                self.loginError = true
            })
        },
    },
    mounted () {
        var state = this.makeState(30)
        this.urlClaveUnica = `https://accounts.claveunica.gob.cl/accounts/login/?next=/openid/authorize%3Fclient_id%3D1c43d493c1294d4982e0be68c363af91%26redirect_uri%3Dhttps%253A%252F%252Fportal.satisfaccion.gob.cl%252Fcallback%26scope%3Dopenid%2Brun%2Bname%26response_type%3Dcode%26state%3D${state}`
    }
}
</script>
<style scoped>

/* Boton estilo de base */
.btn-cu {
  /*display: inline-block;*/
  display: flex;
  justify-content: center;
  font-family: Roboto, sans-serif;
  font-weight: 400;
  text-align: center;
  vertical-align: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  border-radius: 0;
  cursor: pointer;
}

/*Icono ClaveÚnica*/
.btn-cu .cl-claveunica {
  display: inline;
  float: left;
  text-indent: -9999px;
}
/*Texto ClaveÚnica*/
.btn-cu .texto {
  padding-left: 3px;
  text-decoration: underline;
}

/* Tamaño S */
.btn-cu.btn-s {
  width: 130px;
  min-width: 130px;
  height: 36px;
  padding: 8px 10px !important;
  font-size: 14px;
}

.btn-cu.btn-s .cl-claveunica {
  width: 20px;
  height: 20px;
  background-size: 20px 20px;
}

/* Tamaño M */
.btn-cu.btn-m {
  width: 160px;
  /* min-width: 160px; */
  height: 42px;
  padding: 8px 18px 8px 15px !important;
  font-size: 16px;
  line-height: 1.6em;
}

.btn-cu.btn-m .cl-claveunica {
  display: inline-block;
  width: 24px;
  height: 24px;
  background-size: 24px 24px;
}

/* Tamaño L */
.btn-cu.btn-l {
  width: 180px;
  min-width: 180px;
  height: 48px;
  padding: 11px 18px !important;
  font-size: 18px;
}

.btn-cu.btn-l .cl-claveunica {
  width: 26px;
  height: 26px;
  background-size: 26px 26px;
}

/* Tamaño fluid-width */
.btn-cu.btn-fw {
  max-width: 550px;
  width: 100%;
  display: flex;
  justify-content: center;
}
/* Color Estandar */
.btn-cu.btn-color-estandar {
  background-color: #0f69c4;
  color: #fff;
}
.btn-cu.btn-color-estandar .cl-claveunica {
  background: url("/cu/cu-blanco.svg");
}
.btn-cu.btn-color-estandar:hover {
  background-color: #0c549c;
  color: #fff;
}

.btn-cu.btn-color-estandar:active {
  background-color: #093f75;
  color: #fff;
}

.btn-cu.btn-color-estandar:focus {
  background-color: #0c549c;
  color: #fff;
  outline: 1px dashed #000;
}
</style>
