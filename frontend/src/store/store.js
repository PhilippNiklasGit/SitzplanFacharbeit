import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    displayLogin: true,
    displayRegister: false,
    isLoggedIn: false
  },
  mutations: {
    switchOff(state, stateName) {
      switch(stateName){
        case 'isLoggedIn':
          state.isLoggedIn=false
          break;
        case 'displayRegister':
          state.displayRegister=false
          break;
        case 'displayLogin':
          state.displayLogin=false
          break;
      }
    },
    switchOn(state, stateName) {
      switch(stateName){
        case 'isLoggedIn':
          state.isLoggedIn=true
          break;
        case 'displayRegister':
          state.displayRegister=true
          break;
        case 'displayLogin':
          state.displayLogin=true
          break;
      }
    }
  },
  getters : {
    getIsLoggedIn : state => state.isLoggedIn,
    getDisplayLogin : state => state.displayLogin,
    getDisplayRegister : state => state.displayRegister
  }
})