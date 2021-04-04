<template>
  <div>
    <b-container>
      <b-row cols="3">
        <b-col  v-for="(plan, index) in api_plans" v-bind:key="index">
          <b-card :title="plan.title" style="margin-top:5em;">
          <b-button-group>
            <b-button v-on:click="openEdit(plan.plan_id)">Open</b-button>
            <b-button variant="danger" v-on:click="showDeleteModal(plan.plan_id)">Delete</b-button>
          </b-button-group>
          </b-card>  
        </b-col>
        <b-col v-if="api_plans.length<6">
          <b-card style="margin-top:5em;">
            <b-form-input v-model="new_plan_title" style="margin-bottom:1em;"/>
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
      api_ip: (this.$store.getters.getHostLocal ? 'http://127.0.0.1:8000/' : 'http://192.168.179.135:8000/'),
      api_request: {},
      api_plans : [],
      lstorage : window.localStorage,
      new_plan_title : '',
      id_to_delete : null,
    }
  },
  async mounted() {
    var data = await this.axios({
      method: 'get',
      url: this.api_ip + 'api/plans/',
      data: '', 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
    })
    this.api_request = data
    
    this.api_plans = data.data
  },
  methods: {
    openEdit(id_plan_to_open) {
      this.$store.commit('set', {val_name : 'planToEdit', val_new : id_plan_to_open})
      this.$store.commit('switchOff', 'displayManager')
      this.$store.commit('switchOn', 'displayEditor')
    },
    async createNewPlan() {
      if(this.new_plan_title=='') {
        return;
      }
      var new_data = {
        'title' : this.new_plan_title,
        'plan' : []
      }
      var res = await this.axios({
      method: 'post',
      url: this.api_ip + 'api/plans/',
      data: new_data, 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
      })

      this.api_plans.push(res.data)
      this.new_plan_title = ''
    },
    async deletePlan() {
      await this.axios({
      method: 'delete',
      url: this.api_ip + 'api/plans/' + this.id_to_delete + '/',
      data: '', 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
      })
      var ret_val = this.plans.filter(x => {
        if(x.plan_id!=this.id_to_delete) {
          return x;
        }
      })

      this.api_plans = ret_val
    },
    showDeleteModal (id_plan_to_open) {
      this.id_to_delete = id_plan_to_open
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