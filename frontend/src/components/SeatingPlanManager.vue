<template>
  <div>
    <b-container>
      <b-row cols="3">
        <b-col v-for="(plan, index) in api_plans" v-bind:key="index">
          <b-card :title="plan.title" style="margin-top:5em;">
            <b-button-group>
              <b-button v-on:click="openEdit(plan.plan_id)">Open</b-button>
              <b-button
                variant="danger"
                v-on:click="showDeleteModal(plan.plan_id)"
                >Delete</b-button
              >
            </b-button-group>
          </b-card>
        </b-col>
        <b-col v-if="api_plans.length < 6">
          <b-card style="margin-top:5em;">
            <b-form-input v-model="new_plan_title" style="margin-bottom:1em;" />
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
var _ = require("lodash");

export default {
  data() {
    return {
      api_ip: this.$store.getters.getHostLocal // conditional declaration of the api_ip
        ? "http://127.0.0.1:8000/" // localhost
        : "http://192.168.179.135:8000/", // ip host
      api_plans: [], // extracted plans from user data
      new_plan_title: "", // var which is used to be bound to new plan input field
      id_to_delete: null, // id of the plan which is to be delteted if delete button has been pressed
      lstorage: window.localStorage // link to local storage
    };
  },
  async mounted() {
    // api request to get the plans of the recently logged in user
    let api_request = await this.axios({
      method: "get",
      url: this.api_ip + "api/plans/",
      data: "",
      headers: {
        Authorization: "Token " + this.lstorage.getItem("token")
      }
    });

    // extractation of plans from requested data
    this.api_plans = api_request.data
  },
  methods: {
    openEdit(id_plan_to_open) {
      // setting the plan that is to be edited globally (in store)
      this.$store.commit("set", {
        val_name: "planToEdit",
        val_new: id_plan_to_open
      });
      // hide manager
      //show editor
      this.$store.commit("switchOff", "displayManager");
      this.$store.commit("switchOn", "displayEditor");
    },

    async createNewPlan() {
      // abort creation if title is empty
      if (_.isEmpty(this.new_plan_title)) return;

      // create object with data for the new plan => to be inserted in the api
      let new_plan_data = {
        title: this.new_plan_title,
        plan: []
      };

      // send api post request to create a new plan
      let plan_creating_request = await this.axios({
        method: "post",
        url: this.api_ip + "api/plans/",
        data: new_plan_data,
        headers: {
          Authorization: "Token " + this.lstorage.getItem("token")
        }
      });
      // push api response (which now contains an id) to the local plans array  
      this.api_plans.push(plan_creating_request.data);
      // reset the new plan title to empty
      this.new_plan_title = "";
    },

    async deletePlan() {
      // send api request to delete selected plan
      await this.axios({
        method: "delete",
        url: this.api_ip + "api/plans/" + this.id_to_delete + "/",
        data: "",
        headers: {
          Authorization: "Token " + this.lstorage.getItem("token")
        }
      });

      // remove the plan with the matching id
      _.remove(this.api_plans, plan => { return plan.plan_id===this.id_to_delete })

      // alter array to update DOM
      this.api_plans.push({})
      this.api_plans.pop()
    },

    showDeleteModal(id_plan_to_open) {
      // select plan => set id_to_delte to id of the selected plan
      this.id_to_delete = id_plan_to_open;
      // show the delte modal
      this.$refs["delte-modal"].show();
    },

    hideDeleteModal() {
      // hide delte modal
      this.$refs["delete-modal"].hide();
    }
  }
};
</script>

<style>
div {
  color: #000;
}
</style>
