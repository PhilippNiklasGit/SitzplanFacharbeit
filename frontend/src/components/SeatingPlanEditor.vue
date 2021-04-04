<template>
  <div>
    <b-container>
      <b-button
        v-on:click="goBack()"
        style="margin-top: 1em; margin-bottom: 2em;"
        >back</b-button
      >
      <b-button
        variant="danger"
        v-if="!delete_mode && edit_possible"
        v-on:click="toggleDeleteMode()"
        style="margin-top: 1em; margin-bottom: 2em; margin-left: 1em;"
        >activate delete</b-button
      >
      <b-button
        variant="success"
        v-if="delete_mode"
        v-on:click="toggleDeleteMode()"
        style="margin-top: 1em; margin-bottom: 2em; margin-left: 1em;"
        >de-activate delete</b-button
      >
      <b-button
        variant="success"
        v-if="!delete_mode && edit_possible"
        v-on:click="printToPdf()"
        style="margin-top: 1em; margin-bottom: 2em; margin-left: 1em;"
        >print pdf</b-button
      >
      <div id="print-pdf" style="padding: 2px 2px 2px 2px">
        <b-row
          class="grid"
          style="display:grid; min-width:55em; margin-bottom:10em"
        >
          <b-col
            class="my-col"
            v-for="(student, index) in renderable_plan"
            v-bind:key="index"
            ref="grid-ref"
            style="padding: 0px 0px 0px 0px"
          >
            <b-card class="my-card">
              <keep-alive>
                <p
                  v-if="!student.edit"
                  v-on:click="toggleEditOrDelete(student, index)"
                >
                  {{ student.name }}
                </p>
              </keep-alive>
              <p
                v-if="!student.edit && student.name == null"
                class="create-new"
                v-on:click="toggleEditOrDelete(student, index)"
              >
                create new
              </p>
              <b-form-input
                v-if="student.edit"
                v-model="student.name"
                class="name-input"
                :ref="'refs-' + index"
              ></b-form-input>
              <b-button v-if="student.edit" v-on:click="submitEdit(student)"
                >change</b-button
              >
            </b-card>
          </b-col>
        </b-row>
      </div>
    </b-container>
  </div>
</template>

<script>
// import librarys used to generate Pdf
import html2canvas from "html2canvas";
import jsPDF from "jspdf";

export default {
  data() {
    return {
      api_ip: this.$store.getters.getHostLocal // conditional declaration of the api_ip
        ? "http://127.0.0.1:8000/" // localhost
        : "http://192.168.179.135:8000/", // ip host
      plan: {}, // plan which only contains students => programmed to always mirror the version of the backend
      renderable_plan: [], // computed plan which has empty fillers inbetwenn the students to render them onto the DOM
      plan_properties: {}, // properties of the plan which are returned by thhe api
      delete_mode: false, // switch which is used to give the programm the ability to decide if it should delete values or make them editable
      edit_possible: true, // switch that is used to check if there are any ongoing processes which would make a edit impossible
      lstorage: window.localStorage // local storage to save token
    };
  },
  async mounted() {
    // get plan and plan properties from backend api
    let request_return = await this.axios({
      method: "get",
      url: this.api_ip + "api/plans/" + this.$store.getters.getPlanToEdit + "/",
      data: "",
      headers: {
        Authorization: "Token " + this.lstorage.getItem("token")
      }
    });

    // save api return in associated programm variable
    this.plan_properties = request_return.data;
    // save api return in associated programm variable
    this.plan = request_return.data.plan;
    // use data to genreate renderable version of the plan
    this.renderable_plan = this.generateRenderPlan();
  },
  methods: {
    goBack() {
      // hide editor
      //show manager
      // remove current plan id from store
      this.$store.commit("switchOff", "displayEditor");
      this.$store.commit("switchOn", "displayManager");
      this.$store.commit("set", { val_name: "planToEdit", val_new: -1 });
    },

    generateRenderPlan() {
      // initialise array in which the renderable plan will be saved
      let renderable_plan = [];

      // 1-8 for loop in 1-8 for loop to simulate 8x8 grid
      // used fill seats in seating plan with either students from the api or empty values if seat is empty
      for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
          // format current numbers to chars to get ids (1 + 4 => "AD" = tablename)
          let table_id =
            String.fromCharCode(i + 65) + String.fromCharCode(j + 65);
          // map over every stundent in the database / api request
          let id_element = this.plan.filter(x => {
            // check if seat  which is currently being filled matches with anyone of them
            if (x.tablename === table_id) {
              // return student to be filled in the renderable plan
              return x;
            }
          });
          // execute if there is a student on the currently checked seat
          if (id_element[0]) {
            // cast api return values to saveable object
            let new_element = {
              tablename: id_element[0].tablename,
              name: id_element[0].firstname + " " + id_element[0].lastname,
              student_id: id_element[0].student_id,
              edit: false
            };
            // push student into the renderable plan
            renderable_plan.push(new_element);
          } else {
            // cast generated empty values into object
            const new_element = {
              tablename: table_id,
              name: null,
              edit: false
            };
            // push "empty" object into the renderable plan
            renderable_plan.push(new_element);
          }
        }
      }
      // return the plan to be saved in component scoped array
      return renderable_plan;
    },

    toggleOnEdit(index) {
      if (index.name == null) {
        index.edit = true;
        this.edit_possible = false;
      }
    },

    async toggleEditOrDelete(index, index_number) {
      // abort edit toggle if edit action is currently impossible => delete wouldn't be possible aswell
      if (!this.edit_possible) return;

      // remove the element if delete mode is currently in action
      if (this.delete_mode) {
        this.removeElement(index);
        // return to stop function from executing edit actions after the deletion
        return;
      }
      // edit the Element
      this.enableEditForElement(index, index_number);
    },

    async removeElement(index) {
      // send delete api request to the backend to remove the element
      var url = this.api_ip + "api/students/" + index.student_id + "/";
      await this.axios({
        method: "delete",
        url: url,
        data: "",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + this.lstorage.getItem("token")
        }
      });

      // remove element from the renderable plan to prevent it from falsely rendering
      this.renderable_plan.map(x => {
        if (x.tablename == index.tablename) {
          x.name = null;
        }
        return x;
      });

      // push and pop empty element to render plan to force a re-render of the DOM => Vue deosnt re-render array-content changes
      this.renderable_plan.push([]);
      this.renderable_plan.pop();
      return;
    },

    async enableEditForElement(index, index_number) {
      // activate edit mode on currently edited element
      index.edit = !index.edit;

      // if edit mode is entered lock edit_possible to prevent double edits or deltes during edit
      if (index.edit) {
        this.edit_possible = false;
      } else {
        this.edit_possible = true;
      }

      // focus on input field to make edit easier for user => $nextTick because render queue doesnt render input in current tick
      this.$nextTick(() => {
        // get currently editeable element from DOM
        let input_field = this.$refs["refs-" + index_number];
        // focus on Element
        input_field[0].$el.focus();
      });
    },

    async submitEdit(index) {
      // switch edit mode (to off)
      index.edit = !index.edit;

      // enable possible editing since editing is done and about to be submitted
      if (index.edit) {
        this.edit_possible = false;
      } else {
        this.edit_possible = true;
      }

      // check if newly entered name is empty and prevent any api reuqests with empty data
      if (index.name == null) {
        return;
      }

      // get name of student on seat if the seat contained a student
      var name_is = this.plan.filter(x => {
        if (x.tablename === index.tablename) {
          return x;
        }
      });

      // check if seat contained a student and if so, alter student data
      if (name_is[0]) {
        var new_data = this.plan.map(x => {
          if (x.tablename == index.tablename) {
            x.firstname = this.convertToRealName(index.name).firstname;
            x.lastname = this.convertToRealName(index.name).lastname;
            return x;
          } else {
            return x;
          }
        });
      } else {
        // if seat was empty fill it with newly entered data
        this.plan.push({
          tablename: index.tablename,
          firstname: this.convertToRealName(index.name).firstname, // convert to first and lastname and get firstname
          lastname: this.convertToRealName(index.name).lastname // con
        });
        new_data = this.plan;
      }

      // fill object with new updated plan properties and plan
      let new_plan_properties = {
        owner: this.plan_properties.owner,
        plan: new_data,
        plan_id: this.plan_properties.plan_id,
        title: this.plan_properties.title
      };

      // send api request to update the plan / properties
      let plan_update_response = await this.axios({
        method: "put",
        url:
          this.api_ip + "api/plans/" + this.$store.getters.getPlanToEdit + "/",
        data: new_plan_properties,
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + this.lstorage.getItem("token")
        }
      });

      // if seat was empty the newly generated student doesnt posses a student id since they are generated in the database
      // to get this id and save it in the local student object the programm uses the updated response from the backend with the genreated id
      if (!name_is[0]) {
        // filter the response for the student with a matching tablename
        let new_id = plan_update_response.data.plan.filter(x => {
          if (x.tablename == index.tablename) {
            return x;
          }
        });
        // overwrite the student in the reqular plan with the updated version which contains an id
        this.plan.filter(x => {
          if (x.tablename == index.tablename) {
            x["student_id"] = new_id[0].student_id;
          }
        });
        // overwrite the student in the renderable plan with the updated version which contains an id
        this.renderable_plan.filter(x => {
          if (x.tablename == index.tablename) {
            x["student_id"] = new_id[0].student_id;
          }
        });
      }
    },
    // helper function used to store names in the database
    convertToRealName(name) {
      // initialisation of return values
      let firstname = name;
      let lastname = "";
      // check that returns with empty lastname if only firstname is given => prevents assignment errors
      if (name.split(" ").length < 2) return { firstname, lastname };

      // splitting name into two different strings (first and last name)
      name = name.split(" ");
      // getting the last element of the element to save it as the lastname and removing it from the array
      lastname = name[name.length - 1];
      name.pop();
      // joining every element which is still in the array together (precaution for multiple first names)
      firstname = name.join(" ");
      // return object with first and lastname
      return { firstname, lastname };
    },

    toggleDeleteMode() {
      // switch the current delte mode
      this.delete_mode = !this.delete_mode;
    },

    printToPdf() {
      // save current date in variable
      let date = new Date();
      // convert date to date format of the user
      let current_date = date.toLocaleDateString();

      // convert html DOM data to canvas
      html2canvas(document.getElementById("print-pdf")).then(canvas => {
        // cast data of converted canvas to .png and save them in a variable
        let img_data = canvas.toDataURL("image/png", 1.0);
        // initialize empty pdf in landscape orientation
        let pdf = new jsPDF({ orientation: "landscape" });

        // add the title and date above the plan
        pdf.text(5, 10, this.plan_properties.title + " - " + current_date);
        // add the image (data) to the pdf with margins
        pdf.addImage(img_data, "PNG", 20, 15, 250, 220);
        // save the pdf as a file on the users pc with the title of the seating plan being the name of the file
        pdf.save(this.plan_properties.title + ".pdf");
      });
    }
  }
};
</script>

<style>
.create-new {
  transition: opacity 100ms;
  opacity: 0;
}
.create-new:hover {
  opacity: 1;
}

.grid {
  display: grid;
  margin: 0px 0px 0px 0px;
  padding: 0px 0px 0px 0px 0px;
  grid-column-gap: 10px;
  grid-row-gap: 10px;
  grid-template-columns: repeat(8, 1fr);
}

.my-card {
  width: 100%;
  height: 100%;
  padding: 0px 0px 0px 0px;
  margin: 0px 0px 0px 0px;
}

.my-col {
  padding: 0px 0px 0px 0px;
  margin: 0px 0px 0px 0px;
}
</style>
