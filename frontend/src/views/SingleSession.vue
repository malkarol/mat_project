<template>
<div>
  <div class="container mt-3 py-2 border rounded shadow">
    <div class="row">
      <div class="d-flex justify-content-between">
        <div class="col">
          <h2>{{sessionName()}}</h2>
          <div class="d-flex flex-row pt-2 border-bottom">
            <div class="p-2">
              <p class="mb-1"><strong>Owner:</strong></p>
            </div>
            <div class="p-2">
              <p class="mb-1">Karol Malinowski</p>
            </div>
          </div>
        </div>
        <div class="border-bottom align-self-end">
          <p class="text-primary"><strong>IN PROGRESS</strong></p>
        </div>
      </div>
    </div>
    <div class="row py-3">
      <div class="col">
        <div class="row">
        <nav>
          <div class="nav nav-tabs" id="nav-tab" role="tablist">
            <button class="nav-link active" id="nav-home-tab" data-bs-toggle="tab" data-bs-target="#nav-home" type="button" role="tab" aria-controls="nav-home" aria-selected="true">Session Details</button>
            <button class="nav-link" id="nav-contact-tab" data-bs-toggle="tab" data-bs-target="#nav-contact" type="button" role="tab" aria-controls="nav-contact" aria-selected="false">Learning Management Panel</button>
            <button class="nav-link" id="nav-profile-tab" data-bs-toggle="tab" data-bs-target="#nav-profile" type="button" role="tab" aria-controls="nav-profile" aria-selected="false">Test</button>
          </div>
        </nav>
        <div class="tab-content" id="nav-tabContent">
          <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-home-tab">
          test2
          </div>
          <div class="tab-pane fade" id="nav-profile" role="tabpanel" aria-labelledby="nav-profile-tab">
           test test
          </div>
          <div class="tab-pane fade border" id="nav-contact" role="tabpanel" aria-labelledby="nav-contact-tab">
             <div class="row px-4">
                <div class="row mb-3 pt-3">
                  <label for="formFile" class="col-sm-3 col-form-label"><strong>Path to local dataset</strong></label>
                  <div class="col-sm-8">
                    <input class="form-control" type="file" id="formFile">
                  </div>
                </div>
                <div class="input-group mb-3">
                  <div class="input-group-prepend">
                    <span class="input-group-text" id="">Train/Test dataset split %</span>
                  </div>
                  <input type="text" class="form-control">
                  <input type="text" class="form-control">
                </div>
                <div class="row mb-3 pt-3">
                  <label for="formFile" class="col-sm-3 col-form-label"><strong>Loss function</strong></label>
                  <div class="col-sm-8 px-4">
                    <div class="row mb-3">
                      <select class="form-control">
                        <option>Categorical cross-entropy</option>
                        <option>Sparse Multiclass Cross-Entropy Loss</option>
                        <option>Kullback Leibler Divergence Loss</option>
                      </select>
                    </div>
                  </div>
                </div>
                <div class="row mb-3">
                  <label for="formFile" class="col-sm-3 col-form-label"><strong>Learning rounds</strong></label>
                  <div class="col-sm-3">
                    <input class="form-control" type="text">
                  </div>
                </div>
                <div class="row mb-3 pt-3">
                  <div class="">
                    <form>
                      <div class="form-group files color">
                        <label class="mb-3"><strong>Upload your trained model parameters</strong></label>
                        <input type="file" id="file" ref="file" class="form-control" multiple="" @change="handleFileUpload( $event )">
                      </div>
                      <div class="row">
                        <div class="d-flex flex-row">
                          <div class="mx-3 pt-3">
                            <input type="button" @click="submitFile" class="btn btn-primary" value="Send file"/>
                          </div>
                        </div>
                      </div>
                    </form>
                  </div>
                </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="d-flex flex-row">
            <div class="mx-3 pt-3">
              <button class="btn btn-danger">Leave session</button>
            </div>
          </div>
        </div>
        </div>
      </div>
      <div class="col-4">
        <div class="row">
        </div>
        <div class="row">
          <ul class="list-group px-5">
              <li class="text-center list-group-item"><strong>Active participants</strong></li>
              <li class="list-group-item active">Karol</li>
              <li class="list-group-item">Heniek</li>
              <li class="list-group-item">Zbyszek</li>
              <li class="list-group-item">Marek</li>
              <li class="list-group-item">Piotrek</li>
              <li class="list-group-item">Kuba</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'
export default {
  data(){
    return {
      file: ''
    }
  },
  methods: {
      sessionName(){
        return this.$route.params.name == "" ? "Session preview screen" : this.$route.params.name 
      },
      handleFileUpload(){
        this.file = this.$refs.file
      },
      submitFile(e){
        let formData = new FormData()
        const imagefile = document.querySelector('#file');
        formData.append('files', imagefile.files[0]);
        axios.post( 'upload/', // testowy endpoint
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
        });
        }
        
    }
}
</script>

<style>
.files input {
    outline: 2px dashed #92b0b3;
    outline-offset: -10px;
    -webkit-transition: outline-offset .15s ease-in-out, background-color .15s linear;
    transition: outline-offset .15s ease-in-out, background-color .15s linear;
    padding: 120px 0px 85px 35%;
    text-align: center !important;
    margin: 0;
    width: 100% !important;
}
.files input:focus{     outline: 2px dashed #92b0b3;  outline-offset: -10px;
    -webkit-transition: outline-offset .15s ease-in-out, background-color .15s linear;
    transition: outline-offset .15s ease-in-out, background-color .15s linear; border:1px solid #92b0b3;
 }
.files{ position:relative}
.files:after {  pointer-events: none;
    position: absolute;
    top: 60px;
    left: 0;
    width: 50px;
    right: 0;
    height: 56px;
    content: "";
    background-image: url(https://image.flaticon.com/icons/png/128/109/109612.png);
    display: block;
    margin: 0 auto;
    background-size: 100%;
    background-repeat: no-repeat;
}
.color input{ background-color:#f1f1f1;}
.files:before {
    position: absolute;
    bottom: 10px;
    left: 0;  pointer-events: none;
    width: 100%;
    right: 0;
    height: 57px;
    content: " or drag it here. ";
    display: block;
    margin: 0 auto;
    color: #2ea591;
    font-weight: 600;
    text-transform: capitalize;
    text-align: center;
}
</style>
