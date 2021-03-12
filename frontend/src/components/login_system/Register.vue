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


      <b-form-group
        id="input-group-3"
        label-for="input-3"
        description="Password check"
      >
      <b-form-input
          id="input-3"
          v-model="form.password_check"
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
          v-model="form.email"
          
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
      ip: 'http://192.168.179.135:8000/',
      form: {
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
      event.preventDefault()
      
      console.log('huh')
      if (this.form.password!=this.form.password_check) {
        this.alert = 'Your passwords do not match!'
        this.showDismissibleAlert = true
        this.showAlert()

        return;
      }

      const login_data = {
        'username' : this.form.username,
        'password' : this.form.password,
        'email' : this.form.email
      }
      var data = {}
      console.log(login_data)
      const double_data = await this.axios.post(this.ip + 'api/auth/register', login_data)
      .then(function(response) {data = response})
      .catch(err => {
        console.log(err)
        return 'error'
        })

      if(double_data=='error') {
        this.alert = 'This Username already exists!'
        this.showDismissibleAlert = true
        this.showAlert()
        return;
      }
      localStorage.setItem('token', data.data.token)
      this.$store.commit('switchOn', 'isLoggedIn')
      this.$store.commit('switchOff', 'displayLogin')
      this.$store.commit('switchOff', 'displayRegister')
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
  p {
  color: #000;
  }
</style>