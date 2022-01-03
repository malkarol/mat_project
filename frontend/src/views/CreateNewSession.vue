<template>
<div class="col-sm-9 col-md-7 col-lg-8 mx-auto">
  <div class="card border-0 shadow rounded-3 my-5">
    <div class="card-body p-4 p-sm-5 mb-5">
      <div>
        <h3>New session panel</h3>
          <hr />
      </div>
     <form>
  <div class="row mb-3">
    <label for="sessionName" class="col-sm-2 col-form-label" > <strong>Session name</strong></label>
    <div class="col-sm-10">
      <input type="text" class="form-control" id="sessionName" placeholder="e.g. My first session or Prostate Cancer Detection 2022">
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
    <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
    </div>
  </div>
  <div class="row mb-3">
    <label for="description" class="col-sm-2 col-form-label"> <strong>Participants</strong></label>
    <div class="col-sm-10">
    <div class="form-group mb-3">
    <label class="col-form-label col-sm-2" for="formGroupExampleInput"> Minimum number </label>
    <input type="number" id="formGroupExampleInput"  min="3" max="100" >
  </div>
  <div class="form-group mb-3">
    <label class="col-form-label col-sm-2"  for="formGroupExampleInput2">Maximum number </label>
    <input type="number"   id="formGroupExampleInput2" min="3" max="100">
  </div>
  <div class="form-group mb-3">
    <label for="formGroupExampleInput2">Add by username (optional)</label>
      <TagInput :tags="participants" :name="usersComponentName" :maxInput ="maxParticipants" />

  </div>
    </div>

  </div>









  <fieldset class="row mb-3">
    <legend class="col-form-label col-sm-2 pt-0"><strong>Classification type</strong></legend>
    <div class="col-sm-4">
      <select id="inputState" class="form-select" required  data-width="25%">
              <option value="" selected disabled hidden>Choose...</option>
              <option value="1">Student</option>
              <option value="2">Professor</option>
              <option value="3">Professional</option>
              <option value="4">Hobbyst</option>
            </select>
    </div>
    <legend class="col-form-label col-sm-2 pt-0"><strong>Model</strong></legend>

     <div class="col-sm-4">

        <select id="inputState" class="form-select" required  data-width="25%">
              <option value="" selected disabled hidden>Choose...</option>
              <option value="1">Student</option>
              <option value="2">Professor</option>
              <option value="3">Professional</option>
              <option value="4">Hobbyst</option>
            </select>
    </div>
  </fieldset>

   <fieldset class="row mb-3">
    <legend class="col-form-label col-sm-2 pt-0"><strong>Optimizer</strong></legend>
    <div class="col-sm-4">
      <select id="inputState" class="form-select" required  data-width="25%">
              <option value="" selected disabled hidden>Choose...</option>
              <option value="1">Student</option>
              <option value="2">Professor</option>
              <option value="3">Professional</option>
              <option value="4">Hobbyst</option>
            </select>
    </div>
    <legend class="col-form-label col-sm-2 pt-0"><strong>Loss function</strong></legend>

     <div class="col-sm-4">

        <select id="inputState" class="form-select" required  data-width="25%">
              <option value="" selected disabled hidden>Choose...</option>
              <option value="1">Student</option>
              <option value="2">Professor</option>
              <option value="3">Professional</option>
              <option value="4">Hobbyst</option>
            </select>
    </div>
  </fieldset>
    <fieldset class="row mb-3">
    <legend class="col-form-label col-sm-2 pt-0"><strong>Number of epochs</strong></legend>
    <div class="col-sm-4">
      <select id="inputState" class="form-select" required  data-width="25%">
              <option value="" selected disabled hidden>Choose...</option>
              <option value="1">Student</option>
              <option value="2">Professor</option>
              <option value="3">Professional</option>
              <option value="4">Hobbyst</option>
            </select>
    </div>

  </fieldset>
   <div class="row mb-3">
    <label for="sessionName" class="col-sm-2 col-form-label" > <strong>Date range for learning session</strong></label>
    <div class="col-sm-10">
     <Datepicker v-model="date" range   style="width: 330px;" />
    </div>
  </div>

       <button class="btn btn-danger mx-2" @click="backToSessions()">Cancel</button>
       <button class="btn btn-success">Save</button>
      </form>
    </div>
  </div>
</div>

</template>
<script>
import TagInput from '@/components/TagInput.vue'
import Datepicker from 'vue3-date-time-picker'
import 'vue3-date-time-picker/dist/main.css'
import { ref, onMounted } from 'vue';

export default {
  setup() {
        const date = ref();

        // For demo purposes assign range from the current date
        onMounted(() => {
            const startDate = new Date();
            const endDate = new Date(new Date().setDate(startDate.getDate() + 7));
            date.value = [startDate, endDate];
        })

        return {
            date,
        }
    },
  data () {
    return {
      participants: ['user1', 'user2'],
      tags:['medicine', 'science'],
      params:['loss function = categorical cross-entropy'],
      usersComponentName: 'participants',
      tagsComponentName: 'tags',
      maxParticipants: 5,
      maxTags: 5,
      paramsComponentName: 'parameters in form <param name> = <value>',
      maxParams: 100,

    }
  },
  components:{
    TagInput,
    Datepicker,
  },
  methods: {
      showUsers () {
        console.log("siemka")
        console.log(this.participants)
      },
      printDate(){
        console.log(this.date)
      },
      backToSessions(){
        this.$router.push('/sessions')
      }
    },

}
</script>
