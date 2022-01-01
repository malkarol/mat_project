<template>
<div>
  <div class="container mt-3 py-2 border rounded shadow">
    <div class="row">
      <div class="d-flex justify-content-between">
        <div class="col">
          <h2>Testowa sesja</h2>
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
          <p class="text-primary my-0"><strong>IN PROGRESS</strong></p>
          <p class="my-0">Start date: 08.12.2021</p>
          <p>End date: 12.12.2021</p>
        </div>
      </div>
    </div>
    <div class="row py-3">
      <div class="col">
        <div class="row">
        <nav>
          <div class="nav nav-tabs" id="nav-tab" role="tablist">
            <button class="nav-link active" id="nav-contact-tab" data-bs-toggle="tab" data-bs-target="#nav-learning" type="button" role="tab" aria-controls="nav-contact" aria-selected="true">Learning Management Panel</button>
            <button class="nav-link " id="nav-home-tab" data-bs-toggle="tab" data-bs-target="#nav-home" type="button" role="tab" aria-controls="nav-home" aria-selected="false">Session Details</button>
            <button class="nav-link" id="nav-profile-tab" data-bs-toggle="tab" data-bs-target="#nav-profile" type="button" role="tab" aria-controls="nav-profile" aria-selected="false">Results</button>
          </div>
        </nav>
        <div class="tab-content" id="nav-tabContent">
          <div class="tab-pane fade show active border border-top-0" id="nav-learning" role="tabpanel" aria-labelledby="nav-home-tab">
            <div class="row">
              <h5 class="mt-3 px-5"><strong>Description</strong></h5>
              <p class= "mt-3 px-5">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nisl orci, tincidunt id nulla at, maximus aliquet massa. Sed id eros dignissim, laoreet ante et, facilisis neque. Sed sed quam vel odio sagittis tincidunt. Sed velit libero, elementum et felis efficitur, posuere bibendum nisl. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur id tincidunt ligula, sed sodales nisi. Nunc interdum tortor eu molestie finibus.</p>
            </div>
          </div>
          <div class="tab-pane fade border border-top-0" id="nav-profile" role="tabpanel" aria-labelledby="nav-profile-tab">
            Here the user can download the final model and see some statistics
          </div>
          <div class="tab-pane fade border border-top-0" id="nav-contact" role="tabpanel" aria-labelledby="nav-contact-tab">
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
                    <form method="post" action="#" id="#">
                      <div class="form-group files color">
                        <label class="mb-3"><strong>Upload your trained model parameters</strong></label>
                        <input type="file" class="form-control" multiple="">
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
export default {
  props: ['session'],
  data () {
    return {
      text: 'This is an example file to download.'
    }
  },
  methods: {
    downloadText () {
      var blob = new Blob([this.text], { type: 'text/plain' })
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = 'sampleFile.txt'
      link.click()
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
