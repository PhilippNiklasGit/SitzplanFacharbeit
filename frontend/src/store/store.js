import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    displayLogin: true,
    displayRegister: false,
    displayManager: false,
    displayEditor: false,
    isLoggedIn: false,
    planToEdit: -1
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
        case 'displayManager':
          state.displayManager=false
          break;
        case 'displayEditor':
          state.displayEditor=false
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
        case 'displayManager':
          state.displayManager=true
          break;
        case 'displayEditor':
          state.displayEditor=true
          break;
      }
    },
    set(state, val) {
      switch(val.val_name) {
        case 'planToEdit':
          state.planToEdit = val.val_new;
          break;
      }
    }
  },
  getters : {
    getIsLoggedIn : state => state.isLoggedIn,
    getDisplayLogin : state => state.displayLogin,
    getDisplayRegister : state => state.displayRegister,
    getDisplayManager : state => state.displayManager,
    getDisplayEditor : state => state.displayEditor,
    getPlanToEdit : state => state.planToEdit
  }
})