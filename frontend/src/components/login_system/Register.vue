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


      <b-form-group
        id="input-group-3"
        label-for="input-3"
        description="Password check"
      >
      <b-form-input
          id="input-3"
          v-model="user_form.password_check"
          type="password"
          placeholder="Enter password again"
          required
        ></b-form-input>
      </b-form-group>



      <b-form-group
        id="input-group-4"
        label-for="input-4"
        description="email"
      >
      <b-form-input
          id="input-4"
          v-model="user_form.email"
          
          placeholder="Enter email"
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
export default {
  data() {
    return {
      api_ip: (this.$store.getters.getHostLocal ? 'http://127.0.0.1:8000/' : 'http://192.168.179.135:8000/'),
      user_form: {
        username : '',
        password : '',
        password_check : '',
        email : ''
      },
      alert: '',
      dismissSecs: 5,
      dismissCountDown: 0,
      showDismissibleAlert: false,
      storage : window.localStorage
    }
  },
  methods: {
    async onSubmit(event) {
      // prevent site from reloading 
      event.preventDefault()
      
      // check if password has been type correctly twice
      if (this.user_form.password!=this.user_form.password_check) {
        // show alert which notifys the user, that the passwords do not match
        this.alert = 'Your passwords do not match!'
        this.showDismissibleAlert = true
        this.showAlert()
        
        return;
      }

      // get user data from forms and save them for the programm to use
      const login_data = {
        'username' : this.user_form.username,
        'password' : this.user_form.password,
        'email' : this.user_form.email
      }

      // temporary storage to save returned data
      var api_return = {}

      // sends register request to the backend api
      // returns 'error' if failed or session token if the registration request succeded 
      const double_data = await this.axios.post(this.api_ip + 'api/auth/register', login_data)
      .then(function(response) {api_return = response})
      .catch(err => {
        console.log(err)
        // return error to show that the registration failed 
        return 'error'
        })

      // shows alert if username already exists
      if(double_data=='error') {
        this.alert = 'This Username already exists!'
        this.showDismissibleAlert = true
        this.showAlert()
        return;
      }

      // display manager
      // hide login/register
      // set login-token and switch app state to logged in
      localStorage.setItem('token', api_return.data.token)
      this.$store.commit('switchOn', 'isLoggedIn')
      this.$store.commit('switchOff', 'displayLogin')
      this.$store.commit('switchOff', 'displayRegister')
      this.$store.commit('switchOn', 'displayManager')
    },
      onReset(event) {
        // prevent side reaload
        event.preventDefault()

        // reset username and password to empty
        this.user_form.username = ''
        this.user_form.password = ''
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
  p {
  color: #000;
  }
</style>