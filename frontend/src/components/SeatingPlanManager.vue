<template>
  <div>
    <b-container>
      <b-row cols="3">
        <b-col  v-for="(plan, index) in plans" v-bind:key="index">
          <b-card :title="plan.title" style="margin-top:5em;">
          <b-button-group>
            <b-button v-on:click="openEdit(plan.plan_id)">Open</b-button>
            <b-button variant="danger" v-on:click="deletePlan(plan.plan_id)">Delete</b-button>
          </b-button-group>
          </b-card>  
        </b-col>
        <b-col v-if="plans.length<6">
          <b-card style="margin-top:5em;">
            <b-form-input v-model="newPlanTitle" style="margin-bottom:1em;"/>
            <b-button v-on:click="createNewPlan()">Create New +</b-button>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      req: {},
      plans : [],
      lstorage : window.localStorage,
      newPlanTitle : ''
    }
  },
  async mounted() {
    var data = await this.axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/plans/',
      data: '', 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
    })
    this.req = data
    
    this.plans = data.data
  },
  methods: {
    openEdit(planId) {
      console.log(planId)
      this.$store.commit('set', {val_name : 'planToEdit', val_new : planId})
      console.log(this.$store.getters.getPlanToEdit)
      this.$store.commit('switchOff', 'displayManager')
      this.$store.commit('switchOn', 'displayEditor')
    },
    async createNewPlan() {
      if(this.newPlanTitle=='') {
        return;
      }
      var new_data = {
        'title' : this.newPlanTitle,
        'plan' : []
      }
      var res = await this.axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/plans/',
      data: new_data, 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
      })

      this.plans.push(res.data)
      this.newPlanTitle = ''
    },
    async deletePlan(planId) {
      await this.axios({
      method: 'delete',
      url: 'http://127.0.0.1:8000/api/plans/' + planId + '/',
      data: '', 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
      })
      var ret_val = this.plans.filter(x => {
        if(x.plan_id!=planId) {
          return x;
        }
      })

      this.plans = ret_val
    }
  }
}
</script>

<style>
  div {
  color: #000;
  }
</style>