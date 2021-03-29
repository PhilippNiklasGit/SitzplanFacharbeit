<template>
  <div>
    <b-container>
      <b-row cols="3">
        <b-col  v-for="(plan, index) in plans" v-bind:key="index">
          <b-card :title="plan.title" style="margin-top:5em;">
          <b-button-group>
            <b-button v-on:click="openEdit(plan.plan_id)">Open</b-button>
            <b-button variant="danger" v-on:click="showDeleteModal(plan.plan_id)">Delete</b-button>
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
    <b-modal ref="delte-modal" id="delete-modal" @ok="deletePlan()">
    <div class="d-block tex-center">
      <h1>Are you sure, that you want to delete this?</h1>
    </div>
    </b-modal>
  </div>
</template>

<script>
export default {
  data () {
    return {
      ip: 'http://127.0.0.1:8000',
      //ip: 'http://192.168.179.135:8000/',
      req: {},
      plans : [],
      lstorage : window.localStorage,
      newPlanTitle : '',
      idToDelete : null,
    }
  },
  async mounted() {
    var data = await this.axios({
      method: 'get',
      url: this.ip + 'api/plans/',
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
      url: this.ip + 'api/plans/',
      data: new_data, 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
      })

      this.plans.push(res.data)
      this.newPlanTitle = ''
    },
    async deletePlan() {
      await this.axios({
      method: 'delete',
      url: this.ip + 'api/plans/' + this.idToDelete + '/',
      data: '', 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
      })
      var ret_val = this.plans.filter(x => {
        if(x.plan_id!=this.idToDelete) {
          return x;
        }
      })

      this.plans = ret_val
    },
    showDeleteModal (planId) {
      this.idToDelete = planId
      this.$refs['delte-modal'].show()
    },
    hideDeleteModal () {
      this.$refs['delete-modal'].hide()
    }
  }
}
</script>

<style>
  div {
  color: #000;
  }
</style>