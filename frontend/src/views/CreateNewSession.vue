<template>
<div class="col-sm-9 col-md-7 col-lg-8 mx-auto">
    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
        <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z" />
        </symbol>
        <symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16">
            <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z" />
        </symbol>
    </svg>
    <div v-if="errors.length" class="alert alert-danger d-flex align-items-center" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:">
            <use xlink:href="#exclamation-triangle-fill" /></svg>
        <div v-for="error in errors" v-bind:key="error">
            {{ error }}
        </div>
    </div>
    <div class="card border-0 shadow rounded-3 my-5">
        <div class="card-body p-4 p-sm-5 mb-5">
            <div>
                <h3>New session panel</h3>
                <hr>
            </div>
            <form @submit.prevent="submitForm">
                <div class="row mb-3">
                    <h5 for="sessionName" class="col-sm-2 col-form"> <strong>Session name</strong></h5>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="sessionName" placeholder="e.g. My first session or Prostate Cancer Detection 2022" v-model="sessionName">
                    </div>
                </div>
                <div class="row mb-3">
                    <h5 for="pricingPlan" class="col-sm-2 col-form"><strong>Pricing plan</strong></h5>
                    <div class="col-sm-10">
                        <select id="pricingPlan" class="form-select" required v-model="pricing_plan">
                            <option value="" selected disabled hidden>...</option>
                            <option value="0">Free</option>
                            <option value="1">Premium</option>
                        </select>
                    </div>
                </div>
                <div class="row mb-3">
                    <h5 for="tags" class="col-sm-2 col-form"> <strong>Tags</strong></h5>
                    <div class="col-sm-10">
                        <TagInput :tags="tags" :name="tagsComponentName" :maxInput="maxTags" :isUsers="false" />
                    </div>
                </div>

                <div class="row mb-3">
                    <h5 for="description" class="col-sm-2 col-form"> <strong>Description</strong></h5>
                    <div class="col-sm-10">
                        <textarea class="form-control" id="description" rows="3" v-model="description"></textarea>
                    </div>
                </div>
                <div class="row mb-3">
                    <h5 for="description" class="col-sm-2 col-form"> <strong>Participants</strong></h5>
                    <div class="col-sm-10">
                        <div class="form-group mb-3">
                            <label class="col-form col-sm-2" for="minimumNumOfParticipants"> Minimum number </label>
                            <input type="number" id="minimumNumOfParticipants" min="3" max="100" v-model="minNumParticipants">
                        </div>
                        <div class="form-group mb-3">
                            <label class="col-form col-sm-2" for="maximumNumOfParticipants">Maximum number </label>
                            <input type="number" id="maximumNumOfParticipants" min="3" max="100" v-model="maxNumParticipants">
                        </div>
                        <div class="form-group mb-3">
                            <label>Add by username (optional)</label>
                            <TagInput :tags="participants" :name="usersComponentName" :maxInput="maxParticipants" :isUsers="true" />

                        </div>
                    </div>

                </div>


                 <fieldset class="row mb-5">
                     <FixedTable :parameters = "fixedParams" />
                 </fieldset>
                  <fieldset class="row mb-5">
                     <h5 class="col-form col-sm-2 pt-0"><strong>Model Type</strong></h5>

                    <div class="col-sm-4">

                        <select id="modelTypes" class="form-select" required data-width="25%" v-model="modelTypes">
                            <option value="" selected disabled hidden>Choose...</option>
                            <option value="simple_model">Simple models</option>
                            <option value="complex_model">Keras pre-trained models</option>

                        </select>
                    </div>
                 </fieldset>
                 <fieldset v-if="modelTypes == 'complex_model'"  class="row mb-5">
                     <h5 class="col-form col-sm-2 pt-0"><strong>Model name</strong></h5>

                    <div class="col-sm-4">

                        <select @change="getParameters()" id="modelType" class="form-select" required data-width="25%" v-model="modelType" >
                            <option value="" selected disabled hidden >Choose...</option>
                            <option v-for="model in availableModels" :key="model" v-bind:availableModels="availableModels" :value="model">{{model}}</option>
                        </select>
                    </div>
                 </fieldset>
                  <fieldset v-if="modelTypes == 'simple_model'"  class="row mb-5">
                     <h5 class="col-form col-sm-2 pt-0"><strong>Model name</strong></h5>
                <div class="col-sm-4">

                        <select  id="modelType" class="form-select" required data-width="25%" v-model="modelType" >
                            <option value="" selected disabled hidden >Choose...</option>
                            <option value="CNN">Simple CNN</option>
                            <option value="VGG">One block VGG</option>

                        </select>
                    </div>
                  </fieldset>
                 <fieldset v-if="showEditable== true" class="row mb-5">
                     <!-- <EditableTable :responseParams="responseModelParams"/> -->
                 </fieldset>

                <div class="row mb-3">
                    <h5 class="col-sm-2 col-sm-2-pt-0"> <strong>Date range for learning session</strong></h5>
                    <div class="col-sm-10">
                        <Datepicker range style="width: 330px;" v-model="date" />
                    </div>
                </div>
                <div class="d-flex justify-content-between mt-5">
                    <button class="btn btn-success btn-lg px-5">Save</button>
                    <button class="btn btn-danger btn-lg px-5" @click="backToSessions()">Cancel</button>

                </div>
            </form>
            <!-- <button class="btn btn-danger btn-lg px-5" @click="tosth()">tosth</button> -->
        </div>
    </div>
</div>
</template>

<script>
import TagInput from '@/components/TagInput.vue'
import FixedTable from '@/components/FixedTable.vue'
import EditableTable from '@/components/EditableTable.vue'

import Datepicker from 'vue3-date-time-picker'
import 'vue3-date-time-picker/dist/main.css'
import {
    ref,
    onMounted
} from 'vue';
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
    mounted(){
        this.getAvailableModels()
    },
    data() {
        return {
            fixedParams:[{
            name:'number_of_epochs',
            value:5,
            defaultVal: 10,
            Selected: false
        },
        {
            name:'loss_function',
            values:["categorical_crossentropy",
            "sparse_categorical_crossentropy",
            "binary_crossentropy"],
            value: "categorical_crossentropy",
            defaultVal: "categorical_crossentropy",
            Selected: false
        },
        {
            name:'optimizer',
            values:["SGD",
            "RMSprop",
            "Adam",
            "Adadelta",
            "Adagra"
            ],
            value: "SGD",
            defaultVal: "SGD",
            Selected: false
        },
        {
            name:'learning_rate',
            value:0.01,
            defaultVal: 0.01,
            Selected: false

        },
         {
            name:'momentum',
            value:0.9,
            defaultVal: 0.9,
            Selected: false

        },
        {
            name:'batch_size',
            value: 32,
            defaultVal: 32,
            Selected: false


        },
        {
            name:'validation_split',
            value: 0.2,
            defaultVal: 0.2,
            Selected: false

        },
        {
            name:'width_size',
            value:32,
            defaultVal: 32,
            Selected: false

        },
        {
            name:'height_size',
            value:32,
            defaultVal: 32,
            Selected: false

        },
         {
            name:'number_of_classes',
            value:2,
            defaultVal: 2,
            Selected: false

        }],
            responseModelParams:[],
            showEditable:false,
            modelTypes:"",

            // for new session form
            availableModels: [],
            sessionName: '',
            description: '',
            min_num_of_participants: 2,
            max_num_of_participants: 3,
            actual_num_of_participants: 0,
            parameters_keys: [],
            pricing_plan: 0,
            minNumParticipants: 3,
            maxNumParticipants: 5,
            classificationType: '',
            modelType: '',
            optimizer: '',
            lossFunction: '',
            num_of_epochs: 1,

            load_origin: 'local',

            // for tag controls
            participants: [],
            tags: [],
            params: [],

            // for tag controls
            usersComponentName: 'participants',
            tagsComponentName: 'tags',
            paramsComponentName: 'parameters in form <param name> = <value>',
            maxParticipants: 5,
            maxTags: 5,
            maxParams: 100,

            errors: []
        }
    },
    components: {
        TagInput,
        Datepicker,
        FixedTable,
        EditableTable
    },
    methods: {
        updateMyValue(newValue)
        {
            this.fixedParams = newValue
        },
        tosth()
        {
            console.log(this.fixedParams)

        },


         onChange(event) {
            console.log(event.target.value)
        },
        getAvailableModels(){
            axios
                .get('/api/v1/get-available-models/')
                .then(response => {
                    console.log(response.data)
                    this.availableModels = response.data
                }).catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else if (error.message) {
                        this.errors.push('Something went wrong. Please try again.')
                    }
                })
        },
        getParameters() {
            axios
                .get('/api/v1/getparameters/' + this.modelType)
                .then(response => {
                    this.responseModelParams = response.data
                    console.log(response.data)
                    this.showEditable = true
                }).catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else if (error.message) {
                        this.errors.push('Something went wrong. Please try again.')
                    }
                })
        },
        get_many_files() {
            axios({
                url: '/api/v1/get-tar/',
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download', 'somefiles.zip'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                document.body.appendChild(fileLink);

                fileLink.click();

                console.log(response)
            }).catch(error => {
                if (error.response) {
                    for (const property in error.response.data) {
                        this.errors.push(`${property}: ${error.response.data[property]}`)
                    }
                } else if (error.message) {
                    this.errors.push('Something went wrong. Please try again.')
                }
            })
        },
        // testFilterParticipants() {
        //     axios
        //         .get('/api/v1/participants/filter/' + this.$store.state.user.id)
        //         .then(response => {
        //             console.log(response)
        //         }).catch(error => {
        //             if (error.response) {
        //                 for (const property in error.response.data) {
        //                     this.errors.push(`${property}: ${error.response.data[property]}`)
        //                 }
        //             } else if (error.message) {
        //                 this.errors.push('Something went wrong. Please try again.')
        //             }
        //         })
        // },
        // testAddingParticipants() {
        //     const formData = {
        //         usernames: this.participants,
        //         session: 8
        //     }
        //     axios
        //         .post('/api/v1/sessions/', formData)
        //         .then(response => {
        //             console.log(response)
        //         })
        // },
        // showParams() {
        //     var els = document.getElementsByClassName("mlparams");
        //     Array.prototype.forEach.call(els, function (el) {
        //         // Do stuff here

        //         console.log(el.value);
        //     });
        // },

        backToSessions() {
            this.$router.push('/sessions')
        },
        async submitForm() {
            this.errors = []

            if (this.maxNumParticipants <= this.minNumParticipants) {
                this.errors.push("Minimum number of participants cannot be greater than maximum number of participants")
            }
            if (this.num_of_epochs <= 0) {
                this.errors.push("Number of epochs must be a positive number")
            }

            if (this.errors.length > 0) {
                return
            }
            this.parameters_keys = []
            this.parameters_keys.push('model_name')
            this.parameters_keys = this.fixedParams.map(a => a.name);

            this.parameters_values = []
            this.parameters_values.push(this.modelType)
            this.parameters_values = this.fixedParams.map(a => a.value);
            // this.parameters_values.push(this.classificationType)
            // this.parameters_values.push(this.optimizer)
            // this.parameters_values.push(this.lossFunction)
            // this.parameters_values.push(this.num_of_epochs)
            // this.parameters_values.push(this.picture_size)
            // this.parameters_values.push(this.num_of_classes)

            // if (this.color === "1" && this.load_origin === "local") {
            //     this.parameters_values.push('load_color_images')
            // } else if (this.load_origin === "local") {
            //     this.parameters_values.push('load_images')
            // } else {
            //     this.parameters_values.push(this.load_origin)
            // }
            // if (this.color === "1") {
            //     this.parameters_values.push('local_learning')
            //     this.parameters_values.push(3)
            // } else {
            //     this.parameters_values.push('local_learning_b_and_w')
            //     this.parameters_values.push(1)
            // }

            const formData = {
                session: {
                    name: this.sessionName,
                    description: this.description,
                    founder: this.$store.state.user.username,
                    min_num_of_participants: this.minNumParticipants,
                    max_num_of_participants: this.maxNumParticipants,
                    actual_num_of_participants: 1,
                    start_date: this.date[0].toISOString().split('T')[0],
                    end_date: this.date[1] != null ? this.date[1].toISOString().split('T')[0] : null,
                    parameters_keys: this.parameters_keys,
                    parameters_values: this.parameters_values,
                    pricing_plan: this.pricing_plan,
                    tags: this.tags,
                    model_name: this.modelType
                },
                usernames: this.participants

            }
            this.$store.commit('setIsLoading', true)
            await axios
                .post('/api/v1/create-filled-session/', formData)
                .then(response => {

                    console.log(response.data)
                    // // add owner
                    //  const participantData = {
                    //     user: this.$store.state.user.id,
                    //     session: response.data['session_id'],
                    //     is_owner: true
                    //  }
                    // axios
                    // .post('/api/v1/participants/', participantData)
                    // .then(response => {
                    //      console.log(response)
                    // })
                    // .catch( error => {
                    //   if (error.response) {
                    //     for (const property in error.response.data){
                    //       this.errors.push(`${property}: ${error.response.data[property]}`)
                    //     }
                    //   } else if (error.message){
                    //     this.errors.push('Something went wrong. Please try again.')
                    //   }
                    // })

                    // now add participants

                    this.$router.push('/sessions/')
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else if (error.message) {
                        this.errors.push('Something went wrong. Please try again.')
                    }
                })
            this.$store.commit('setIsLoading', false)
        }
    },

}
</script>
