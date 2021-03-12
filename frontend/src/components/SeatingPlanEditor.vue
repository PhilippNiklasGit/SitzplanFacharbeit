<template>
  <div>
    <b-container>
      <b-button v-on:click="goBack()" style="margin-top: 1em; margin-bottom: 2em;">back</b-button>
      <b-button variant="danger" v-if="!deleteMode && deletePossible" v-on:click="toggleDeleteMode()" style="margin-top: 1em; margin-bottom: 2em; margin-left: 1em;">activate delete</b-button>
      <b-button variant="success" v-if="deleteMode" v-on:click="toggleDeleteMode()" style="margin-top: 1em; margin-bottom: 2em; margin-left: 1em;">de-activate delete</b-button>
      <b-button variant="success" v-if="!deleteMode && deletePossible" v-on:click="printToPdf()" style="margin-top: 1em; margin-bottom: 2em; margin-left: 1em;">print pdf</b-button>
      <div id="print-pdf" style="padding: 2px 2px 2px 2px">
      <b-row class="grid" style="display:grid; min-width:55em; margin-bottom:10em">
        <b-col class="my-col" v-for="(student, index) in render_plan" v-bind:key="index" style="padding: 0px 0px 0px 0px">
          <b-card class="my-card">
          <keep-alive>
            <p v-if="!student.edit" v-on:click="toggleEdit(student)">{{ student.name }}</p>
          </keep-alive>
            <p v-if="!student.edit && student.name==null" class="create-new" v-on:click="toggleEdit(student)"> create new</p>
            <b-form-input v-if="student.edit" v-model="student.name"></b-form-input>
            <b-button v-if="student.edit" v-on:click="submitEdit(student)">change</b-button>
          </b-card>
        </b-col>
      </b-row>
      </div>
    </b-container>
  </div>
</template>

<script>
import html2canvas from 'html2canvas'
//import html2pdf from 'html2pdf'
import jsPDF from 'jspdf'
export default {
 data() {
   return {
     ip: 'http://192.168.179.135:8000/',
     plan : {},
     render_plan: [],
     lstorage : window.localStorage,
     data : {},
     deleteMode : false,
     deletePossible : true,
   }
 },
 async mounted() {
    var data = await this.axios({
      method: 'get',
      url: this.ip + 'api/plans/' + this.$store.getters.getPlanToEdit + '/',
      data: '', 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
    })
    this.data = data.data
    this.plan = data.data.plan
    this.generateRenderPlan()
},
 methods: {
   goBack() {
      this.$store.commit('switchOff', 'displayEditor')
      this.$store.commit('switchOn', 'displayManager')
      this.$store.commit('set', {val_name : 'planToEdit', val_new : -1})
   },
   generateRenderPlan() {
     for (let i = 0; i < 8; i++) {
       for (let j = 0; j < 8; j++) {
         var table_id = String.fromCharCode(i+65) + String.fromCharCode(j+65)
         const id_element = this.plan.filter(x => {
           if(x.tablename===table_id) {
            return x
           }
           })
         if(id_element[0]) {
          const new_element = {
           'tablename' : id_element[0].tablename,
           'name' : id_element[0].firstname + ' ' + id_element[0].lastname,
           'student_id' : id_element[0].student_id,
           'edit' : false
          }
          this.render_plan.push(new_element)
         } else {
           const new_element = {
           'tablename' : table_id,
           'name' : null,
           'edit' : false
          }
           this.render_plan.push(new_element)
         }
      }
     }
   },
   toggleOnEdit(index) {
     if(index.name==null) {
       index.edit = true;
       this.deletePossible = false;
     }
   },
   async toggleEdit(index) {
    if(this.deleteMode) {
      var url = this.ip + 'api/students/' + index.student_id + '/'
      await this.axios({
      method: 'delete',
      url: url,
      data: '', 
      headers: {
        'Content-Type' : 'application/json',
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
      })
      
      this.render_plan.map(x => {
        
        if(x.tablename==index.tablename) {
          x.name = null
        }
        return x;
      })
      this.$forceUpdate()
      this.render_plan.push([])
      this.render_plan.pop()
      return;
    } 

    index.edit = !index.edit
    if(index.edit) {
      this.deletePossible = false;
    } else {
      this.deletePossible = true;
    }
     
   },
   async submitEdit(index) {
     index.edit = !index.edit
     if(index.edit) {
      this.deletePossible = false;
    } else {
      this.deletePossible = true;
    }
     var name_is = this.plan.filter(x => {
       if(x.tablename===index.tablename) {
         return x
       }
      })

     if(name_is[0]) {
       var new_data = this.plan.map(x => {
         if(x.tablename==index.tablename) {
           x.firstname = this.convertToRealName(index.name)[0]
           x.lastname = this.convertToRealName(index.name)[1]
           return x
         } else {
           return x
         }
       })
     } else {
      this.plan.push({
        'tablename' : index.tablename,
        'firstname' : this.convertToRealName(index.name)[0],
        'lastname' : this.convertToRealName(index.name)[1]
      })
      new_data = this.plan
     }
     
     
     
     var new_data_put = {
       'owner' : this.data.owner,
       'plan' : new_data,
       'plan_id' : this.data.plan_id,
       'title' : this.data.title
     }
     var url = this.ip + 'api/plans/' + this.$store.getters.getPlanToEdit + '/'
     
     var res = await this.axios({
      method: 'put',
      url: url,
      data: new_data_put, 
      headers: {
        'Content-Type' : 'application/json',
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
      })
      if(!name_is[0]) {
        var new_id = res.data.plan.filter(x => {
          if(x.tablename==index.tablename) {
            return x
          }
        })
        this.plan.filter(x => {
          if(x.tablename==index.tablename) {
            x['student_id'] = new_id[0].student_id
          }
          
        })
        this.render_plan.filter(x => {
          if(x.tablename==index.tablename) {
            x['student_id'] = new_id[0].student_id
          }
          
        })
      }
   },
   convertToRealName(name) {
      if(name.split(' ').length<2) return [name, ""];
      name = name.split(' ');
      var lastname = name[name.length-1]
      name.pop();
      var firstname = name.join(' ');
      return [firstname, lastname];
    },
    toggleDeleteMode() {
      this.deleteMode = !this.deleteMode
    },
    printToPdf() {
      var date = new Date();
      var current_date = date.toLocaleDateString()
      html2canvas(document.getElementById('print-pdf')).then(canvas => {
        var imgData = canvas.toDataURL('image/png', 1.0)
        var pdf = new jsPDF({orientation:'landscape'});

        pdf.text(5,10, this.data.title + ' - ' + current_date)
        pdf.addImage(imgData, 'PNG', 20, 15, 250, 220)
        pdf.save(this.data.title + '.pdf')

      })
    }
 }
}
</script>

<style>
  .create-new {
    opacity: 0;
  }
  .create-new:hover {
    transition-delay: 1s;
    opacity: 1.0;
  }

  .grid {
    display: grid;
    margin: 0px 0px 0px 0px;
    padding: 0px 0px 0px 0px 0px;
    grid-column-gap: 10px;
    grid-row-gap: 10px;
    grid-template-columns: repeat(8, 1fr)
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