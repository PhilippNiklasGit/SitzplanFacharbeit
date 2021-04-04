<template>
  <div>
    <b-form @submit="onSubmit" @onReset="onReset" style="margin-top: 5em;">
      <b-form-group
        id="input-group-1"
        label-for="input-1"
        description="Username"
      >
      <b-form-input
          id="input-1"
          v-model="form.username"
          
          placeholder="Enter username"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-2"
        
        label-for="input-2"
        description="Password"
      >
      <b-form-input
          id="input-2"
          v-model="form.password"
          type="password"
          placeholder="Enter password"
          required
        ></b-form-input>
      </b-form-group>


      <b-button type="submit" >Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>


    <b-alert
      :show="dismissCountDown"
      dismissible
      variant="warning"
      @dismissed="dismissCountDown=0"
      @dismiss-count-down="countDownChanged"
    >
      <p>{{ alert }}</p>
      <b-progress
        variant="danger"
        :max="dismissSecs"
        :value="dismissCountDown"
        height="4px"
      ></b-progress>
    </b-alert>
  </div>
  
</template>

<script>
//import axios from 'axios';

export default {
  data() {
    return {
      api_ip: (this.$store.getters.getHostLocal ? 'http://127.0.0.1:8000/' : 'http://192.168.179.135:8000/'),
      form: {
        username : '',
        password : ''
      },
      storage : window.localStorage,
      alert: '',
      dismissSecs: 5,
      dismissCountDown: 0,
      showDismissibleAlert: false,
    }
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault()
      

      const login_data = {
        'username' : this.form.username,
        'password' : this.form.password
      }
      var data = {}
      
      const error_check = await this.axios.post(this.api_ip + 'api/auth/login', login_data)
      .then(function(response) {data = response})
      .catch(err => {
        console.log(err)
          this.alert = 'your password or username is incorrect!'
          this.showAlert()
          return 'error';
        })

      if(error_check=='error') {
        return;
      }
      localStorage.setItem('token', data.data.token)
      this.$store.commit('switchOn', 'isLoggedIn')
      this.$store.commit('switchOff', 'displayLogin')
      this.$store.commit('switchOff', 'displayLogin')
      this.$store.commit('switchOn', 'displayManager')
    },
      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.username = ''
        this.form.password = ''
      },
      countDownChanged(dismissCountDown) {
        this.dismissCountDown = dismissCountDown
      },
      showAlert() {
        this.dismissCountDown = this.dismissSecs
      }
  }
}
</script>

<style>

</style>