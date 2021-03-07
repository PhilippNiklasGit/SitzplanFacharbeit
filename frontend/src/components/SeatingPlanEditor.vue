<template>
  <div>
    <b-container>
      <b-button v-on:click="goBack()" style="margin-top: 1em; margin-bottom: 2em;">back</b-button>
      <b-button variant="danger" v-if="!deleteMode && deletePossible" v-on:click="toggleDeleteMode()" style="margin-top: 1em; margin-bottom: 2em; margin-left: 1em;">activate delete</b-button>
      <b-button variant="success" v-if="deleteMode" v-on:click="toggleDeleteMode()" style="margin-top: 1em; margin-bottom: 2em; margin-left: 1em;">de-activate delete</b-button>
      <b-row>
      
        <b-col  v-for="(student, index) in render_plan" v-bind:key="index" style="color:#fff;margin-right:0em; padding-right:0em;padding-left:0em;margin-bottom:1em;">
          <b-card style="width: 8em; margin-right:0em; padding-right:0em;">
          <keep-alive>
            <p v-if="!student.edit" v-on:click="toggleEdit(student)">{{ student.name }}</p>
          </keep-alive>
            <p v-if="!student.edit && student.name==null" class="create-new" v-on:click="toggleEdit(student)"> create new</p>
            <b-form-input v-if="student.edit" v-model="student.name"></b-form-input>
            <b-button v-if="student.edit" v-on:click="submitEdit(student)">change</b-button>
          </b-card>
          
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
      url: 'http://127.0.0.1:8000/api/plans/' + this.$store.getters.getPlanToEdit + '/',
      data: '', 
      headers: {
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
    })
    this.data = data.data
    this.plan = data.data.plan
    console.log(this.plan)
    this.generateRenderPlan()
    console.log(this.plan)
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
     console.log(index.name)
     if(index.name==null) {
       index.edit = true;
       this.deletePossible = false;
     }
   },
   async toggleEdit(index) {
    if(this.deleteMode) {
      var url = 'http://127.0.0.1:8000/api/students/' + index.student_id + '/'
      await this.axios({
      method: 'delete',
      url: url,
      data: '', 
      headers: {
        'Content-Type' : 'application/json',
        Authorization: 'Token ' + this.lstorage.getItem('token')
      }
      })
      
      console.log(index)
      var test = this.render_plan.map(x => {
        console.log(x)
        
        if(x.tablename==index.tablename) {
          x.name = null
        }
        return x;
      })
      console.log(test)
      console.log('yeet')
      this.$forceUpdate()
      this.render_plan.push([])
      this.render_plan.pop()
      return;
    } 

    index.edit = !index.edit
    console.log('heloooow')
    console.log(index)
    if(index.edit) {
      console.log('bruhhh')
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
       console.log('eyo')
       console.log(x)
       if(x.tablename===index.tablename) {
         return x
       }
      })
      console.log(name_is)
      console.log('yeah')
     if(name_is[0]) {
       var new_data = this.plan.map(x => {
         console.log(x)
         console.log()
         if(x.tablename==index.tablename) {
           x.firstname = this.convertToRealName(index.name)[0]
           x.lastname = this.convertToRealName(index.name)[1]
           return x
         } else {
           return x
         }
       })
     } else {
       console.log(index.name)
      this.plan.push({
        'tablename' : index.tablename,
        'firstname' : this.convertToRealName(index.name)[0],
        'lastname' : this.convertToRealName(index.name)[1]
      })
      new_data = this.plan
     }
     
     console.log(this.data)
     
     
     var new_data_put = {
       'owner' : this.data.owner,
       'plan' : new_data,
       'plan_id' : this.data.plan_id,
       'title' : this.data.title
     }
     console.log(new_data_put)
     var url = 'http://127.0.0.1:8000/api/plans/' + this.$store.getters.getPlanToEdit + '/'
     
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
        console.log(res)
        var new_id = res.data.plan.filter(x => {
          if(x.tablename==index.tablename) {
            return x
          }
        })
        this.plan.filter(x => {
          if(x.tablename==index.tablename) {
            console.log(new_id)
            x['student_id'] = new_id[0].student_id
          }
          
        })
        this.render_plan.filter(x => {
          if(x.tablename==index.tablename) {
            console.log(new_id)
            x['student_id'] = new_id[0].student_id
          }
          
        })
        console.log(this.plan)
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
    }
 }
}
</script>

<style>
  .create-new {
    opacity: 0;
  }
  .create-new:hover {
    opacity: 1.0;
  }
</style>