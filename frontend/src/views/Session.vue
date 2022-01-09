<template>
    <div class="col-sm-9 col-md-7 col-lg-10 mx-auto">
        <div class="card border-0 shadow rounded-3 my-5">
            <div class="card-body p-4 p-sm-5 mb-5">
                <div>
                    <h2>{{this.session.name}}</h2>
                    <hr />
                </div>
                <nav>
                 <div class="nav nav-tabs mb-4" id="nav-tab" role="tablist">
            <button class="nav-link active" id="nav-home-tab" data-bs-toggle="tab" data-bs-target="#nav-home" type="button" role="tab" aria-controls="nav-home" aria-selected="true">General information</button>
            <button class="nav-link" id="nav-upload-tab" data-bs-toggle="tab" data-bs-target="#nav-upload" type="button" role="tab" aria-controls="nav-upload" aria-selected="false">Upload your local model</button>
            <button class="nav-link" id="nav-getGlobal-tab" data-bs-toggle="tab" data-bs-target="#nav-getGlobal" type="button" role="tab" aria-controls="nav-getGlobal" aria-selected="false">Get global model</button>
          </div>
          </nav>

        <div class="tab-content" id="nav-tabContent">
          <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-home-tab">
              <div class="row">
              <div class="col-md order-md-2">
                <form >
                <div class="row mx-3">
                    <div class="col shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                         <h4 for="lastName" class="d-flex justify-content-center"> <strong>Session deadline</strong></h4>
                         <div class="d-flex justify-content-around">
                         <h5 class="d-flex justify-content-centery"> {{this.session.start_date}}</h5>
                         <h5 class="d-flex justify-content-centery"> {{this.session.end_date == null ? "No end date" : this.session.end_date}} </h5>
                         </div>
                         </div>
                    </div>
                    <div class="row mx-3">

                            <div class="col shadow p-3 mb-5 rounded" style="background-color: #f1f1f1;">
                            <h4 for="lastName" class="d-flex justify-content-center"> <strong>Participants</strong></h4>
                            <ul v-for="(participant, index) in participants" :key="participant.username" class="list-group px-5 rounded">
                            <li class="list-group-item" :style="styleFounder(participant.username)"> {{index + 1}} <hr /><div> <h6>  {{participant.username}}</h6>
                  <small class="text-muted">{{getUserType(participant.usertype)}}</small>
                  </div></li>

                             </ul>


                            </div>
                    </div>



            </form>
              </div>
        <div class="col-md-7 order-md-1">
            <form >
                <div class="row">
                    <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                        <h4 for="lastName"> <strong>Description</strong></h4>
                        <p >
                            {{this.session.description}}
                        </p>
                    </div>
                </div>
                <div class="row">
                    <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                    <div v-for="(tag) in session.tags" :key="tag">
                <h4> <strong> Tags </strong> </h4>
                <hr />
                 <span class="badge bg-dark mx-1"> {{tag}} </span>

                </div>
                    </div>
                </div>
                 <div class="row">
                    <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                        <h4> <strong> Parameters </strong> </h4>
                        <hr />
                        <table  class="table table-bordered table-hover">
                          <thead>
                            <tr>
                              <th scope="col">#</th>
                              <th scope="col">Parameter</th>
                              <th scope="col">Value</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(parameter, index) in session.parameters_keys" :key="parameter">
                              <th scope="row">{{index}}</th>
                              <td>{{parameter}}</td>
                              <td>{{session.parameters_values[index]}}</td>
                            </tr>

                          </tbody>
                        </table>
                <!-- <fieldset class="row mb-2">
                    <legend class="col-form-label col-sm-2 pt-0"><strong>Classification type</strong></legend>
                    <div class="col-sm-4">
                        <label class="d-flex justify-content-center"> Image</label>
                    </div>

                    <legend class="col-form-label col-sm-2 pt-0"><strong>Model</strong></legend>
                <div class="col-sm-4">
                    <label class="d-flex justify-content-center"> Simple Multi-layer Perceptor</label>
                </div>
            </fieldset>
            <hr />
              <fieldset class="row mb-2">
                    <legend class="col-form-label col-sm-2 pt-0"><strong>Optimizer</strong></legend>
                    <div class="col-sm-4">
                    <label class="d-flex justify-content-center"> Stochiastic Gradient Descent</label>
                    </div>
                    <legend class="col-form-label col-sm-2 pt-0"><strong>Loss function</strong></legend>

                <div class="col-sm-4">
                     <label class="d-flex justify-content-center"> categorical crossentropy</label>

                </div>
            </fieldset>
            <hr />
             <fieldset class="row mb-2 ">
                    <legend class="col-form-label col-sm-2 pt-0"><strong>Number of local epochs</strong></legend>
                    <div class="col-sm-4">
                        <label class="d-flex justify-content-center"> 4</label>
                    </div>

            </fieldset> -->

                    </div>
                 </div>
            </form>
            <button class="btn btn-primary btn-lg btn-success mb-3" @click="backToSessions()">Download script for this parameters</button>
        </div>
              </div>
                </div>
                 <div class="tab-pane fade" id="nav-upload" role="tabpanel" aria-labelledby="nav-upload-tab">
             <div class="col-md-8 order-md-1">
            <div class="row mt-3">

            <p  class="form-control-plaintext col mb-3 shadow p-3 mb-5 text-danger rounded " style="background-color: #f1f1f1;" id="staticText"
            > <strong>Important !!! </strong>
            <br> At the bottom of previous tab, called <strong>General information</strong>, you could generate a configurated Python script with model implementation.
            <br> At this tab you are expected to upload a file that contains weights of pretrained model and were generated by mentioned script.
            <br> Of course it should be in <strong>.h5 format</strong>.
            </p>
            </div>
            <form >
                <div class="row mt-3">
                    <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                         <h4 for="lastName"> <strong>Local model upload:</strong></h4>
                         <div>
                            <label for="formFileLg" class="form-label text-muted" >(Only .h5 files)</label>
                            <input class="form-control form-control-lg" id="formFileLg" accept=".h5" type="file">
                        </div>
                         <input type="button" class="btn btn-primary btn-lg btn-success mt-3" @click="submitFile" value="Upload local model"/>
                         </div>
                    </div>



            </form>

        </div>
                </div>

          <div class="tab-pane fade" id="nav-getGlobal" role="tabpanel" aria-labelledby="nav-getGlobal-tab">
               <div class="row mt-3">
                    <div class="col mb-3 shadow p-3 mb-5 d-flex justify-content-center rounded" style="background-color: #f1f1f1;">
                <button class="btn btn-primary btn-lg btn-success mt-3 mb-3 mx-1" @click="getFile()">Download global model</button>
                <button class="btn btn-primary btn-lg btn-success mt-3 mb-3 mx-1" @click="backToSessions()">Aggregate models</button>
                <button class="btn btn-primary btn-lg btn-success mt-3 mb-3 mx-1" @click="backToSessions()">Show results</button>
                    </div>
               </div>

          </div>
           </div>
 <button class="btn btn-primary btn-lg btn-block" @click="backToSessions()">Back to sessions</button>
</div>
            </div>
        </div>

</template>
<style>

</style>
<script>
// import participantJson from '@/participants.json'
import axios from 'axios'


export default {
    data() {
        return {
            // participantList: participantJson,
            startDate: '2022-01-01',
            endDate: '2022-02-01',
            session: {},
            participants:[],



        }
    },
    mounted() {
       axios.get('/api/v1/session/'+this.$route.params.id).then(response => {
            this.session = response.data

        }).catch( error => {
            if (error.response) {
              for (const property in error.response.data){
                this.errors.push(`${property}: ${error.response.data[property]}`)
              }
            } else if (error.message){
              this.errors.push('Something went wrong. Please try again.')
            }
          })

          axios.get('/api/v1/participants/session/'+this.$route.params.id).then(response => {
            this.participants =response.data
            this.participants.sort(function(a, b) {
              return parseFloat(a.user_id) - parseFloat(b.user_id);
            })

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
    methods:
    {
        styleFounder (username){
            if(username === this.session.founder)
            {
                return "background-color: #ffc34d;"
            }
        },
        getUserType (usertype){
           switch (usertype) {
                case 0:
                    return "Student"
                case 1:
                    return "Professor"
                case 2:
                    return "Professional"
                case 3:
                    return "Hobbyst"
                default:
                  return "none"
            }
        },
        backToSessions () {
            this.$router.push('/sessions/')
        },
        sessionName(){
        return this.$route.params.name == "" ? "Session preview screen" : this.$route.params.name
        },
        submitFile(e){
            let formData = new FormData()
            const imagefile = document.querySelector('#formFileLg');
            formData.append('files', imagefile.files[0]);
            formData.append('session_id', this.session.session_id)
            console.log(formData)
            axios.post( 'upload/', // testowy endpoint - to zrob zeby nie byl testowy
              formData,
              {
                headers: {
                    'Content-Type': 'multipart/form-data'
              }
            }
            ).then(function(){
              console.log('SUCCESS!!');
            })
            .catch(function(){
              console.log('FAILURE!!');
            })
        },
        getFile(){
            console.log(this.session)

            axios({
                  url: 'download/' + this.session.session_id,
                  method: 'GET',
                  responseType: 'blob',
              }).then((response) => {
                    var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                    var fileLink = document.createElement('a');

                    fileLink.href = fileURL;
                    fileLink.setAttribute('download', 'file.pdf'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                    document.body.appendChild(fileLink);

                    fileLink.click();

                    console.log(response)
              })
        }
    }
}
// <div class="form-group ">
//                         <label class="row mb-3"><strong>Upload your local model</strong></label>
//                         <input type="file" multiple @change="uploadFile"/>
//       <div @drop="dragFile" >
//         Or drag the file here
//         <div v-if="File.length">
//           <ul v-for="file in File" :key="file">
//             <li>{{file.name}}</li>
//           </ul>
//         </div>
//       </div>
//                         </div>
</script>
