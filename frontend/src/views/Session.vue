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
                    <button v-if="this.session.founder == this.$store.state.user.username" class="nav-link" id="nav-manageSession-tab" data-bs-toggle="tab" data-bs-target="#nav-manageSession" type="button" role="tab" aria-controls="nav-manageSession" aria-selected="false">Manage session</button>
                </div>
            </nav>

            <div class="tab-content" id="nav-tabContent">
                <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-home-tab">
                    <div class="row">
                        <div class="col-md order-md-2">
                            <form>
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
                                            <li class="list-group-item" :style="styleFounder(participant.username)"> {{index + 1}}
                                                <hr />
                                                <div class="d-flex flex-row justify-content-between">
                                                    <div>
                                                        <h6> {{participant.username}}</h6>
                                                        <small class="text-muted">{{getUserType(participant.usertype)}}</small>
                                                    </div>
                                                    <button @click="removeParticipant(participant)" v-if="this.session.founder == this.$store.state.user.username && participant.username != this.session.founder" data-toggle="tooltip" data-placement="top" title="Remove participant from session" type="button" class="btn-close" aria-label="Close"></button>
                                                </div>
                                            </li>

                                        </ul>

                                    </div>
                                </div>

                            </form>
                        </div>
                        <div class="col-md-7 order-md-1">
                            <form>
                                <div class="row">
                                    <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                        <h4 for="lastName"> <strong>Description</strong></h4>
                                        <p>
                                            {{this.session.description}}
                                        </p>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                        <div>
                                            <h4> <strong> Tags </strong> </h4>
                                            <hr />
                                            <span v-for="(tag) in session.tags" :key="tag" class="badge bg-dark mx-1"> {{tag}} </span>

                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                        <h4> <strong> Parameters </strong> </h4>
                                        <hr />
                                        <table class="table table-bordered table-hover">
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
                            <div class="row">
                                <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                    <div>
                                        <label for="uploadWeights" class="form-label text-muted">Only .h5 files.</label>
                                        <input class="form-control form-control-lg" id="uploadWeights" accept=".h5" type="file">
                                    </div>
                                    <input type="button" class="btn btn-primary btn-lg btn-success mt-3" @click="initializeGlobalWeightsScript()" value="Get script to calculate global weights" />
                                    <input type="button" class="btn btn-primary btn-lg btn-success mt-3 mx-5" @click="uploadGlobalWeights()" value="Upload global weights" />

                                </div>
                            </div>
                            <button class="btn btn-primary btn-lg btn-success mb-3" @click="generateLocalModel()">Download script for this parameters</button>
                            <button class="btn btn-primary btn-lg btn-success mb-3" @click="getInitialWeights()">Get initial weights</button>

                        </div>
                    </div>
                </div>
                <div class="tab-pane fade" id="nav-upload" role="tabpanel" aria-labelledby="nav-upload-tab">
                    <div class="col-md-8 order-md-1">
                        <div class="row mt-3">

                            <p class="form-control-plaintext col mb-3 shadow p-3 mb-5 text-danger rounded " style="background-color: #f1f1f1;" id="staticText"> <strong>Important !!! </strong>
                                <br> At the bottom of previous tab, called <strong>General information</strong>, you could generate a configurated Python script with model implementation.
                                <br> At this tab you are expected to upload a file that contains weights of pretrained model and were generated by mentioned script.
                                <br> Of course it should be in <strong>.h5 format</strong>.
                            </p>
                        </div>
                        <form>
                            <div class="row mt-3">
                                <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                    <h4 for="lastName"> <strong>Upload weights from local model:</strong></h4>
                                    <div>
                                        <label for="uploadLocal" class="form-label text-muted">(Only .h5 files)</label>
                                        <input class="form-control form-control-lg" id="uploadLocal" accept=".h5" type="file">
                                    </div>
                                    <input type="button" class="btn btn-primary btn-lg btn-success mt-3 mb-3" @click="uploadLocalWeights()" value="Upload local weights" />
                                    <div>
                                        <label for="uploadLocalJson" class="form-label text-muted">(Only .json files)</label>
                                        <input class="form-control form-control-lg" id="uploadLocalJson" accept=".json" type="file">
                                    </div>
                                    <input type="button" class="btn btn-primary btn-lg btn-success mt-3" @click="uploadLocalWeightsJson()" value="Upload local weights" />
                                </div>
                            </div>
                            <div class="row mt-3">
                                <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                    <h4 for="lastName"> <strong>Upload results file:</strong></h4>
                                    <div>
                                        <label for="uploadLocalResults" class="form-label text-muted">(Only .json files)</label>
                                        <input class="form-control form-control-lg" id="uploadLocalResults" accept=".json" type="file">
                                    </div>
                                    <input type="button" class="btn btn-primary btn-lg btn-success mt-3" @click="LocalLearningResults()" value="Upload results" />
                                </div>
                            </div>

                        </form>

                    </div>
                </div>

                <div class="tab-pane fade" id="nav-getGlobal" role="tabpanel" aria-labelledby="nav-getGlobal-tab">
                    <div class="row mt-3">
                        <div class="col mb-3 shadow p-3 mb-5 d-flex justify-content-center rounded" style="background-color: #f1f1f1;">
                            <div>
                                <button class="btn btn-primary btn-lg btn-success d-inline p-2 mb-2 mx-2" @click="getFile()">Global model script for predictions</button>
                                <button class="btn btn-primary btn-lg btn-success d-inline p-2 mb-2 mx-2" @click="getGlobalModel()">Global model script for idividual learning</button>
                            </div>
                            <div>
                                <button class="btn btn-primary btn-lg btn-success d-inline p-2 mb-2 mx-2" @click="getAggregateModelsScript()">Aggregate models locally</button>
                                <button class="btn btn-primary btn-lg btn-success d-inline p-2 mb-2 mx-2" @click="getAggregation()">Aggregate models on server</button>

                            </div>
                            <div>
                                <button class="btn btn-primary btn-lg btn-success d-inline p-2 mb-2 mx-2" @click="getManyWeights()">Get local weights</button>
                                <button class="btn btn-primary btn-lg btn-success d-inline p-2 mb-2 mx-2" @click="backToSessions()">Show results</button>
                            </div>

                        </div>
                    </div>

                </div>
                <div v-if="this.session.founder == this.$store.state.user.username" class="tab-pane fade" id="nav-manageSession" role="tabpanel" aria-labelledby="nav-manageSession-tab">
                    <div class="row mt-3">
                        <div class="col mb-3 shadow p-3 mb-5 d-flex justify-content-center rounded" style="background-color: #f1f1f1;">
                            <button class="btn btn-primary btn-lg btn-success mt-3 mb-3 mx-1" @click="deleteSession()">Delete session</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="d-flex justify-content-between">
                <button class="btn btn-primary btn-lg btn-block" @click="backToSessions()">Back to sessions</button>
                <button v-if="session.founder != this.$store.state.user.username" class="btn btn-danger btn-lg btn-block" @click="leaveSession()">Leave session</button>
            </div>
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
            participants: [],
            errors: [],
            data_path: ''

        }
    },
    mounted() {
        axios.get('/api/v1/session/' + this.$route.params.id)
            .then(response => {
                this.session = response.data

            }).catch(error => {
                if (error.response) {
                    for (const property in error.response.data) {
                        this.errors.push(`${property}: ${error.response.data[property]}`)
                    }
                } else if (error.message) {
                    this.errors.push('Something went wrong. Please try again.')
                }
            })

        axios.get('/api/v1/participants/session/' + this.$route.params.id).then(response => {
            this.participants = response.data

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
    methods: {
        styleFounder(username) {
            if (username === this.session.founder) {
                return "background-color: #ffc34d;"
            }
        },
        getUserType(usertype) {
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
        leaveSession() {
            if (!confirm("Are you sure you wish to leave this session?"))
                return
            axios.delete('api/v1/leavesession/' + this.session.session_id)
                .then(response => {
                    this.backToSessions()
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
        },
        deleteSession() {
            if (confirm("Are you sure you would like to delete this session? This action cannot be undone.")){
                axios.delete('api/v1/session/' + this.session.session_id)
                .then(response => {
                    this.backToSessions()
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
            }
        },
        removeParticipant(participant) {
            axios.delete('api/v1/session/' + this.session.session_id + '/participant/' + participant.user_id)
                .then(response => {
                    console.log(response)
                    axios.get('/api/v1/participants/session/' + this.$route.params.id).then(response => {
                        this.participants = response.data
                        this.participants.sort(function (a, b) {
                            return parseFloat(a.user_id) - parseFloat(b.user_id);
                        })

                    }).catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again.')
                        }
                    })
                })
                .catch(error => {
                    console.log(error)
                })
        },
        backToSessions() {
            this.$router.push('/sessions/')
        },
        sessionName() {
            return this.$route.params.name == "" ? "Session preview screen" : this.$route.params.name
        },
        submitFile(e) {
            let formData = new FormData()
            const imagefile = document.querySelector('#formFileLg');
            formData.append('files', imagefile.files[0]);
            formData.append('session', this.session.session_id)
            console.log(formData)
            axios.post('upload/', // testowy endpoint - to zrob zeby nie byl testowy
                    formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                ).then(function () {
                    console.log('SUCCESS!!');
                })
                .catch(function () {
                    console.log('FAILURE!!');
                })
        },
        getAggregation() {
            axios.get('/api/v1/aggregate-on-server/' + this.$route.params.id)
                .then(response => {
                    this.session = response.data

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
        LocalLearningResults() {
            const imagefile = document.querySelector('#uploadLocalResults');

            let formData = new FormData()
            formData.append('files', imagefile.files[0]);
            formData.append('session', this.session.session_id)

            axios.post('/api/v1/upload-local-results-json/', // testowy endpoint - to zrob zeby nie byl testowy
                    formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                ).then(function () {
                    console.log('SUCCESS!!');
                })
                .catch(function () {
                    console.log('FAILURE!!');
                })
        },
        getManyWeights() {
            console.log(this.participants[0].username)
            const array = this.participants; // changed the input array a bit so that the `array[i].id` would actually work - obviously the asker's true array is more than some contrived strings
            let users = [];
            let promises = [];
            for (let i = 0; i < array.length; i++) {
                promises.push(
                    axios.get('/api/v1/get-global-weights/' + this.session.session_id).then(response => {
                        // do something with response
                        const fileURL = window.URL.createObjectURL(new Blob([response.data]));
                        const fileLink = document.createElement('a');

                        fileLink.href = fileURL;
                        fileLink.setAttribute('download', `local_weights_${this.participants[i].username}.h5`); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                        document.body.appendChild(fileLink);

                        fileLink.click();
                    })
                )
            }

            Promise.all(promises).then(() => console.log(users));
        },
        uploadLocalWeightsJson() {
            const imagefile = document.querySelector('#uploadLocalJson');

            let formData = new FormData()
            formData.append('files', imagefile.files[0]);
            formData.append('session', this.session.session_id)

            axios.post('/api/v1/upload-local-weights-json/', // testowy endpoint - to zrob zeby nie byl testowy
                    formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                ).then(function () {
                    console.log('SUCCESS!!');
                })
                .catch(function () {
                    console.log('FAILURE!!');
                })
        },
        getInitialWeights() {
            axios({
                url: '/api/v1/get-global-weights/' + this.session.session_id,
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download', 'initial_weights.h5'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                document.body.appendChild(fileLink);

                fileLink.click();

                console.log(response)
                axios({
                    url: '/api/v1/instructions/lm/',
                    method: 'GET',
                    responseType: 'blob',
                }).then((response) => {
                    var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                    var fileLink = document.createElement('a');

                    fileLink.href = fileURL;
                    fileLink.setAttribute('download', 'instructions.txt'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                    document.body.appendChild(fileLink);

                    fileLink.click();

                    console.log(response)
                })
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
        getFile() {
            axios({
                url: 'api/v1/getzip/' + this.session.session_id,
                //url: 'api/v1/testmodel/',
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                console.log(response)
                var fileURL = window.URL.createObjectURL(new Blob([response.data],{type:'application/zip'}));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download', 'sessiongit.zip'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                document.body.appendChild(fileLink);

                fileLink.click();

                console.log(response)
            })
        },
        generateLocalModel() {

            axios({
                url: '/api/v1/generate-local-model/' + this.session.session_id,
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download', 'local_model.py'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                document.body.appendChild(fileLink);

                fileLink.click();

                console.log(response)
                axios({
                    url: '/api/v1/instructions/lm/',
                    method: 'GET',
                    responseType: 'blob',
                }).then((response) => {
                    var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                    var fileLink = document.createElement('a');

                    fileLink.href = fileURL;
                    fileLink.setAttribute('download', 'instructions.txt'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                    document.body.appendChild(fileLink);

                    fileLink.click();

                    console.log(response)
                })
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
        getLocalModelInstructions() {
            console.log(heh)
            axios({
                url: '/api/v1/instructions/lm/',
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                var fileURL2 = window.URL.createObjectURL(new Blob([response.data]));
                var fileLink2 = document.createElement('a');

                fileLink2.href = fileURL2;
                fileLink2.setAttribute('download', 'instructions.txt'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                document.body.appendChild(fileLink2);

                fileLink2.click();

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
        getAggregateModelsScript() {
            axios({
                url: '/api/v1/generate-aggregate-script/' + this.session.session_id,
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download', 'aggregation_script.py'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                document.body.appendChild(fileLink);

                fileLink.click();

                console.log(response)
                axios({
                    url: '/api/v1/instructions/lm/',
                    method: 'GET',
                    responseType: 'blob',
                }).then((response) => {
                    var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                    var fileLink = document.createElement('a');

                    fileLink.href = fileURL;
                    fileLink.setAttribute('download', 'instructions.txt'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                    document.body.appendChild(fileLink);

                    fileLink.click();

                    console.log(response)
                })
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
        getGlobalModel() {
            axios({
                url: '/api/v1/generate-global-model/' + this.session.session_id,
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download', 'global_model.py'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                document.body.appendChild(fileLink);

                fileLink.click();

                console.log(response)
                axios({
                    url: '/api/v1/instructions/lm/',
                    method: 'GET',
                    responseType: 'blob',
                }).then((response) => {
                    var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                    var fileLink = document.createElement('a');

                    fileLink.href = fileURL;
                    fileLink.setAttribute('download', 'instructions.txt'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                    document.body.appendChild(fileLink);

                    fileLink.click();

                    console.log(response)
                })
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
        getGlobalModelForPredictions() {

        },
        uploadLocalWeights() {
            const imagefile = document.querySelector('#uploadLocal');

            let formData = new FormData()
            formData.append('files', imagefile.files[0]);
            formData.append('session', this.session.session_id)

            axios.post('/api/v1/upload-local-model/', // testowy endpoint - to zrob zeby nie byl testowy
                    formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                ).then(function () {
                    console.log('SUCCESS!!');
                })
                .catch(function () {
                    console.log('FAILURE!!');
                })
        },
        uploadGlobalWeights() {
            const imagefile = document.querySelector('#uploadWeights');

            let formData = new FormData()
            formData.append('files', imagefile.files[0]);
            formData.append('session', this.session.session_id)

            axios.post('/api/v1/upload-global-weights/', // testowy endpoint - to zrob zeby nie byl testowy
                    formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                ).then(function () {
                    console.log('SUCCESS!!');
                })
                .catch(function () {
                    console.log('FAILURE!!');
                })
        },
        initializeGlobalWeightsScript() {

            axios({
                url: '/api/v1/generate-weights-script/' + this.session.session_id,
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                var fileURL = window.URL.createObjectURL(new Blob([response.data]));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download', 'initialize_weights.py'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
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
