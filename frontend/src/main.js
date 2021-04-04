import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue } from 'bootstrap-vue'
import store from './store/store.js'
import VueAxios from 'vue-axios'
import axios from 'axios'



import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(VueAxios, axios)



new Vue({
  store: store,
  render: h => h(App),
}).$mount('#app')
