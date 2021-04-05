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
          v-model="user_form.username"
          
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
          v-model="user_form.password"
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
      user_form: {
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
      // prevent reloding of site on submit
      event.preventDefault()
      
      // get login data from html form and save it for the programm to use
      const login_data = {
        'username' : this.user_form.username,
        'password' : this.user_form.password
      }

      // temporary storage to save returned data
      let api_response = {}
      
      // sends login request to the backend api
      // returns 'error' if failed or session token if the login request succeded 
      const error_check = await this.axios.post(this.api_ip + 'api/auth/login', login_data)
      .then(function(response) {api_response = response})
      .catch(err => {
        console.log(err)
          this.alert = 'your password or username is incorrect!'
          this.showAlert()
          // return error to show that the login failed
          return 'error';
        })
      
      // prevent login if login request failed
      if(error_check=='error') {
        return;
      }

      // display manager
      // hide login
      // set login-token and switch app state to logged in
      localStorage.setItem('token', api_response.data.token)
      this.$store.commit('switchOn', 'isLoggedIn')
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