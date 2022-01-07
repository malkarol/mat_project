<template>
<div class="col-sm-9 col-md-7 col-lg-8 mx-auto">
  <div class="card border-0 shadow rounded-3 my-5">
    <div class="card-body p-4 p-sm-5 mb-5">
      <div>
        <h3>New session panel</h3>
          <hr />
      </div>
     <form @submit.prevent="submitForm">>
  <div class="row mb-3">
    <label for="sessionName" class="col-sm-2 col-form-label" > <strong>Session name</strong></label>
    <div class="col-sm-10">
      <input type="text" class="form-control" id="sessionName" placeholder="e.g. My first session or Prostate Cancer Detection 2022" v-model="sessionName">
    </div>
  </div>
   <div class="row mb-3">
    <label for="tags" class="col-sm-2 col-form-label"> <strong>Tags</strong></label>
    <div class="col-sm-10">
      <TagInput :tags="tags" :name="tagsComponentName" :maxInput="maxTags" />
    </div>
  </div>



  <div class="row mb-3">
    <label for="description" class="col-sm-2 col-form-label"> <strong>Description</strong></label>
    <div class="col-sm-10">
    <textarea class="form-control" id="description" rows="3"  v-model="description"></textarea>
    </div>
  </div>
  <div class="row mb-3">
    <label for="description" class="col-sm-2 col-form-label"> <strong>Participants</strong></label>
    <div class="col-sm-10">
    <div class="form-group mb-3">
    <label class="col-form-label col-sm-2" for="minimumNumOfParticipants"> Minimum number </label>
    <input type="number" id="minimumNumOfParticipants"  min="3" max="100" v-model="minNumParticipants">
  </div>
  <div class="form-group mb-3">
    <label class="col-form-label col-sm-2"  for="maximumNumOfParticipants">Maximum number </label>
    <input type="number" id="maximumNumOfParticipants" min="3" max="100"  v-model="maxNumParticipants">
  </div>
  <div class="form-group mb-3">
    <label >Add by username (optional)</label>
      <TagInput :tags="participants" :name="usersComponentName" :maxInput ="maxParticipants" />

  </div>
    </div>

  </div>









  <fieldset class="row mb-3">
    <legend class="col-form-label col-sm-2 pt-0" ><strong>Classification type</strong></legend>
    <div class="col-sm-4">
      <select id="classificationType" class="form-select mlparams" required  data-width="25%" v-model="classificationType">
              <option value="" selected disabled hidden>Choose...</option>
              <option value="image">Image</option>
              <option value="text">Text</option>
            </select>
    </div>
    <legend class="col-form-label col-sm-2 pt-0"><strong>Model</strong></legend>

     <div class="col-sm-4">

        <select id="modelType" class="form-select" required  data-width="25%" v-model="modelType">
              <option value="" selected disabled hidden>Choose...</option>
              <option value="SimpleMLP">SimpleMLP</option>
              <option value="CNN">CNN</option>
            </select>
    </div>
  </fieldset>

   <fieldset class="row mb-3">
    <legend class="col-form-label col-sm-2 pt-0"><strong>Optimizer</strong></legend>
    <div class="col-sm-4">
      <select id="optimizer" class="form-select mlparams" required  data-width="25%" v-model="optimizer">
              <option value="" selected disabled hidden>Choose...</option>
              <option value="SGD">SGD</option>
              <option value="RMSprop">rmsprop</option>
            </select>
    </div>
    <legend class="col-form-label col-sm-2 pt-0"><strong>Loss function</strong></legend>

     <div class="col-sm-4">

        <select id="lossFunction" class="form-select mlparams" required  data-width="25%" v-model="lossFunction">
              <option value="" selected disabled hidden>Choose...</option>
              <option value="binary_crossentropy">binary_crossentropy</option>
              <option value="categorical_crossentropy">categorical_crossentropy</option>
            </select>
    </div>
  </fieldset>
    <fieldset class="row mb-3">
    <legend class="col-form-label col-sm-2 pt-0"><strong>Number of epochs</strong></legend>
    <div class="col-sm-4">
      <input class = "mlparams" type="number" id="numOfEpochs"  min="1" max="100" v-model="num_of_epochs">
    </div>

  </fieldset>
   <div class="row mb-3">
    <label class="col-sm-2 col-form-label" > <strong>Date range for learning session</strong></label>
    <div class="col-sm-10">
     <Datepicker  range  style="width: 330px;" v-model="date"/>
    </div>
  </div>

       <button class="btn btn-danger mx-2" @click="backToSessions()">Cancel</button>
       <button class="btn btn-success">Save</button>

      </form>
      <button class="btn btn-success" @click="testFilterParticipants()">kurde bele </button>
    </div>
  </div>
</div>

</template>
<script>
import TagInput from '@/components/TagInput.vue'
import Datepicker from 'vue3-date-time-picker'
import 'vue3-date-time-picker/dist/main.css'
import { ref, onMounted } from 'vue';
import axios from 'axios'
export default {
  setup() {
        const date = ref();

        // For demo purposes assign range from the current date
        onMounted(() => {
            const startDate = new Date();
            const endDate = null;
            //const endDate = new Date(new Date().setDate(startDate.getDate() + 7));
            date.value = [startDate, endDate];
        })

        return {
            date,
        }
    },
  data () {
    return {

      // for new session form
      sessionName: '',
      description: '',
      min_num_of_participants: 2,
      max_num_of_participants: 3,
      actual_num_of_participants: 0,
      parameters_keys: ['classification_type', 'optimizer','loss_function','num_of_epochs'],
      pricing_plan : 0,
      minNumParticipants: 3,
      maxNumParticipants: 5,
      classificationType: '',
      modelType: '',
      optimizer: '',
      lossFunction:'',
      num_of_epochs:1,



      // for tag controls
      participants: [],
      tags:[],
      params:[],

      // for tag controls
      usersComponentName: 'participants',
      tagsComponentName: 'tags',
      paramsComponentName: 'parameters in form <param name> = <value>',
      maxParticipants: 5,
      maxTags: 5,
      maxParams: 100,

    }
  },
  components:{
    TagInput,
    Datepicker,
  },
  methods: {
    testFilterParticipants (){
         axios
          .get('/api/v1/participants/filter/' + this.$store.state.user.id)
          .then(response => {
            console.log(response)
          }).catch( error => {
            if (error.response) {
              for (const property in error.response.data){
                this.errors.push(`${property}: ${error.response.data[property]}`)
              }
            } else if (error.message){
              this.errors.push('Something went wrong. Please try again.')
            }
          })
      },
      testAddingParticipants (){
        const formData = {
          usernames:this.participants,
          session: 8
        }
         axios
          .post('/api/v1/sessions/', formData)
          .then(response => {
            console.log(response)
          })
      },
      showParams () {
        var els = document.getElementsByClassName("mlparams");
        Array.prototype.forEach.call(els, function(el) {
        // Do stuff here

        console.log(el.value);
        });
      },
      showUsers () {
        console.log("siemka")
        console.log(this.participants)
      },
      printDate(){
        console.log(this.date)
      },
      backToSessions(){
        this.$router.push('/sessions')
      },
      async submitForm () {
      this.errors = []

      this.parameters_values =  []
      this.parameters_values.push(this.classificationType)
      this.parameters_values.push(this.optimizer)
      this.parameters_values.push(this.lossFunction)
      this.parameters_values.push(this.num_of_epochs)
      const formData = {
        name: this.sessionName,
        description: this.description,
        founder: this.$store.state.user.id,
        min_num_of_participants: this.maxNumParticipants,
        max_num_of_participants: this.minNumParticipants,
        actual_num_of_participants: 1,
        start_date: this.date[0].toISOString().split('T')[0],
        end_date: this.date[1] !=null ? this.date[1].toISOString().split('T')[0] : null,
        parameters_keys: this.parameters_keys,
        parameters_values: this.parameters_values,
        pricing_plan: 0,
        tags: this.tags,
        model_name: this.modelType

      }
      this.$store.commit('setIsLoading', true)
      await axios
          .post('/api/v1/sessions/', formData)
          .then(response => {


            console.log(response.data)
            // add owner
             const participantData = {
                user: this.$store.state.user.id,
                session: response.data['session_id'],
                is_owner: true
             }
          axios
          .post('/api/v1/participants/', participantData)
          .then(response => {
               console.log(response)
          })
          .catch( error => {
            if (error.response) {
              for (const property in error.response.data){
                this.errors.push(`${property}: ${error.response.data[property]}`)
              }
            } else if (error.message){
              this.errors.push('Something went wrong. Please try again.')
            }
          })

            // now add participants

            this.$router.push('/sessions/')
          })
          .catch( error => {
            if (error.response) {
              for (const property in error.response.data){
                this.errors.push(`${property}: ${error.response.data[property]}`)
              }
            } else if (error.message){
              this.errors.push('Something went wrong. Please try again.')
            }
          })
          this.$store.commit('setIsLoading', false)
    }
    },

}
</script>
