<template>
  <div id="app">
    <b-navbar type="primary" variant="dark">
      <b-navbar-nav>Sitzplan Designer</b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-button-group>
          <b-button variant="dark" v-if="!this.$store.getters.getIsLoggedIn" size="sm" v-on:click="display('login')">Login</b-button>
          <b-button variant="dark" v-if="!this.$store.getters.getIsLoggedIn" size="sm" v-on:click="display('register')">Register</b-button>
        </b-button-group>
        <b-button variant="dark" v-if="this.$store.getters.getIsLoggedIn" size="sm" v-on:click="logout()">Logout</b-button>
      </b-navbar-nav>
    </b-navbar>

    <b-container fluid="sm">
      <Login v-if="this.$store.getters.getDisplayLogin"/>
      <Register v-if="this.$store.getters.getDisplayRegister"/>
      <SeatingPlanManager v-if="this.$store.getters.getDisplayManager"/>
      <SeatingPlanEditor v-if="this.$store.getters.getDisplayEditor" />
    </b-container>
  </div>
</template>

<script>
import Login from './components/login_system/Login.vue'
import Register from './components/login_system/Register.vue'
import SeatingPlanManager from './components/SeatingPlanManager.vue'
import SeatingPlanEditor from './components/SeatingPlanEditor.vue'

export default {
  name: 'App',
  components: {
    Login,
    Register,
    SeatingPlanManager,
    SeatingPlanEditor
  },
  data() {
    return {
      ip: 'http://192.168.179.135:8000/',
      lstorage : window.localStorage
    }
  },
  async mounted(){
    if(!this.lstorage.getItem('token')) return;
    var error;
    await this.axios({
      method: 'get',
      url: this.ip + 'api/auth/user',
      data: '', 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
    }).catch(err => {error = err})
    
    if(!error) {
      this.$store.commit('switchOn', 'isLoggedIn')
      this.$store.commit('switchOff', 'displayLogin')
      this.$store.commit('switchOff', 'displayRegister')
      this.$store.commit('switchOn', 'displayManager')
    }
  },
  methods: {
    display(to_display) {
      switch (to_display) {
        case 'login':
          this.$store.commit('switchOn', 'displayLogin')
          this.$store.commit('switchOff', 'displayRegister')
          break;
        case 'register':
          this.$store.commit('switchOn', 'displayRegister')
          this.$store.commit('switchOff', 'displayLogin')
          break;
      }
    },
    async logout() {
      var config = {
        headers : {
          'Authorization' : 'Token ' + this.lstorage.getItem('token')
        }
      }
      await this.axios.post('http://127.0.0.1:8000/api/auth/logout', '', config)
      this.lstorage.removeItem('token')
      this.$store.commit('switchOff', 'isLoggedIn')
      this.$store.commit('switchOn', 'displayLogin')
    }
  },
  
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #fff;
}
</style>
