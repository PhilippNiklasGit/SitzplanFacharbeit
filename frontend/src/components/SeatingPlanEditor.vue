<template>
  <div>
    <b-container>
      <b-button v-on:click="goBack()">back</b-button>
      <b-row cols="8">
        <b-col v-for="(student, index) in plan" v-bind:key="index">
          {{ student.firstname }} {{ student.lastname }}
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
 data() {
   return {
     plan : {},
     lstorage : window.localStorage
   }
 },
 async mounted() {
    var data = await this.axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/plans/' + this.$store.getters.getPlanToEdit + '/',
      data: '', 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
    })
    this.plan = data.data.plan
    //this.plan = data.data
 },
 methods: {
   goBack() {
      this.$store.commit('switchOff', 'displayEditor')
      this.$store.commit('switchOn', 'displayManager')
      this.$store.commit('set', {val_name : 'planToEdit', val_new : -1})
   }
 }
}
</script>

<style>

</style>