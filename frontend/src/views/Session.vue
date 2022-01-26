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
                    <button class="nav-link active" id="nav-home-tab" data-bs-toggle="tab" data-bs-target="#nav-home" type="button" role="tab" aria-controls="nav-home" aria-selected="true">Information</button>
                    <button class="nav-link" id="nav-upload-tab" data-bs-toggle="tab" data-bs-target="#nav-upload" type="button" role="tab" aria-controls="nav-upload" aria-selected="false">Learning panel</button>
                    <button v-if="showResultsTab || debug" class="nav-link" id="nav-getGlobal-tab" data-bs-toggle="tab" data-bs-target="#nav-getGlobal" type="button" role="tab" aria-controls="nav-getGlobal" aria-selected="false">Results</button>
                </div>
            </nav>

            <div v-if="!this.$store.state.isLoading" class="tab-content" id="nav-tabContent">
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
                                                    <td>{{this.getParamName(parameter)}}</td>
                                                    <td>{{session.parameters_values[index]}}</td>
                                                </tr>

                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </form>

                        </div>
                    </div>
                </div>
                <div class="tab-pane fade" id="nav-upload" role="tabpanel" aria-labelledby="nav-upload-tab">
                    <div class="row">
                        <div class="col-6 px-4">
                            <div v-if="(showStep1 && isActive && !sessionEnded) || debug" class="row">
                                <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                    <h4 for="uploadWeights"> <strong>Step 1. Download learning script</strong></h4>
                                    <p>Download learning script for this model to train it on your private data</p>
                                    <button :disabled="!isActive" class="btn btn-primary btn-lg btn-success  mt-3  " @click="generateLocalModel()">Download local learning script</button>
                                    <div class="text-center mb-3" v-if="downloadingScript">
                                        <div class="lds-dual-ring"></div>
                                        <div>Downloading script and test dataset...</div>
                                    </div>
                                </div>
                            </div>
                            <div v-if="!isActive  && !sessionEnded" class="row">
                                <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                    <h4 for="uploadWeights"> <strong>Wait for session to start</strong></h4>
                                    <p>Learning session has not started yet. Please wait until the session start date: {{this.session.start_date}} or required number of participants join the session to begin learning</p>
                                    <p><strong>Required number of participants to start learning session: {{this.session.min_num_of_participants}}</strong></p>
                                </div>
                            </div>
                            <div v-if="(showStep2 && isActive && !showStep4 && !sessionEnded) || debug" class="row">
                                <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                    <h4 for="uploadWeights"> <strong>Step 2. Wait for other participants to upload their model weights</strong></h4>
                                    <p>Some participants still need to train their local model and upload the weights.</p>
                                </div>
                            </div>
                            <div v-if="(showStep3 && isActive  && !sessionEnded && this.session.founder != this.$store.state.user.username) || debug" class="row">
                                <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                    <h4 for="uploadWeights"> <strong>Step 3. Wait for the session founder to perform aggregation</strong></h4>
                                    <p>...</p>
                                </div>
                            </div>
                            <div v-if="(showStep3 && isActive && !sessionEnded && this.session.founder == this.$store.state.user.username) || debug" class="row">
                                <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                    <h4 for="uploadWeights"> <strong>Step 3. Aggregate your model</strong></h4>
                                    <p>All participants have uploaded their weights. It's time for you to start the aggregation process
                                        to calculate the weights for the final model.</p>
                                    <div class="text-center mb-3" v-if="aggregating">
                                        <div class="lds-dual-ring"></div>
                                        <div>Aggregating...</div>
                                    </div>
                                    <div class="d-flex justify-content-center">
                                        <button class="btn btn-primary btn-lg btn-success d-inline p-2 mb-2 mx-2" @click="getAggregateModelsScript()">Aggregate models locally</button>
                                        <button v-if="this.session.pricing_plan == 1 || debug" class="btn btn-primary btn-lg btn-success d-inline p-2 mb-2 mx-2" @click="getAggregation()">Aggregate models on server</button>
                                    </div>
                                    <h5 class="" v-if="downloadingLocalAggregation"><strong>Downloading weights and test dataset...</strong></h5>
                                </div>
                            </div>
                            <div v-if="(showStep4 && isActive && !sessionEnded)|| debug" class="row">
                                <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                    <h4 for="uploadWeights"> <strong>Step 4. Aggregation process is finished. See the results</strong></h4>
                                    <p>Aggregation process has finished successfully. Go to results tab to see the learning results and download aggregated model weights</p>
                                </div>
                            </div>
                            <div v-if="sessionEnded || debug" class="row">
                                <div class="col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                    <h4> <strong>This session has finished</strong></h4>
                                    <p>This session has already ended. Go to results tab to see the final statistics about this learning session</p>
                                </div>
                            </div>
                            <div class="row mt-3">

                                <!-- <p class="form-control-plaintext col mb-3 shadow p-3 mb-5 text-danger rounded " style="background-color: #f1f1f1;" id="staticText"> <strong>Important !!! </strong>
                                <br> At the bottom of previous tab, called <strong>General information</strong>, you could generate a configurated Python script with model implementation.
                                <br> At this tab you are expected to upload a file that contains weights of pretrained model and were generated by mentioned script.
                                <br> Of course it should be in <strong>.h5 format</strong>.
                            </p> -->
                            </div>
                        </div>
                        <div class="col-5 px-4">
                            <div class="col shadow p-3 rounded" style="background-color: #f1f1f1;">
                                <h4> <strong> Participants' progress for <span class="text-danger">federated round {{this.session.federated_round}}:</span> </strong> </h4>
                                <hr />
                                <table class="table table-bordered table-hover">
                                    <thead>
                                        <tr>
                                            <th scope="col">#</th>
                                            <th class="text-center" scope="col">Participant</th>
                                            <th class="text-center" scope="col">Weights uploaded</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(participant, index) in this.participantsProgress" :key="participant.username">
                                            <th scope="row">{{index+1}}</th>
                                            <td class="text-center">{{participant.user_name}}</td>
                                            <td class="text-center" v-if="participant.is_model_uploaded"><strong>&#10004;</strong></td>
                                            <td class="text-center" v-else><strong>&#10060;</strong></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="tab-pane fade" id="nav-getGlobal" role="tabpanel" aria-labelledby="nav-getGlobal-tab">
                    <div class="">
                        <div class="row mt-3">
                            <!--v-if="this.session.founder == this.$store.state.user.username"-->
                            <!--<div class="col mb-3 shadow p-3 mb-5 rounded" style="background-color: #f1f1f1;">
                                <h4><strong>Available actions for aggregation:</strong></h4>

                            </div>-->
                            <div class="row mt-3">
                                <div class="col mb-3 shadow p-3 mb-5 rounded" style="background-color: #f1f1f1;">
                                    <h4><strong>Federated Averaging:</strong></h4>
                                    <div class=" d-flex justify-content-center">
                                        <button class="btn btn-primary btn-lg btn-success d-inline p-2 mb-2 mx-2" @click="getFile()">Global model script for predictions</button>
                                        <button class="btn btn-primary btn-lg btn-success d-inline p-2 mb-2 mx-2" @click="getGlobalModel()">Global model script for idividual learning</button>
                                        <input type="button" class="btn btn-primary btn-lg btn-success d-inline p-2 mb-2 mx-2" @click="fillData()" value="Show results" />
                                    </div>
                                </div>
                            </div>

                        </div>
                        <div v-if="renderChart" class="row mt-3">
                            <div class="w-100 d-flex col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                <div>
                                    <h4 class='mb-3'> <strong>Accuracy and loss diagrams for round {{this.session.federated_round - 1}}:</strong></h4>
                                    <div class="d-flex justify-content-center">
                                        <ChartResult :key="componentKey" v-bind:chartData="chartDataAccuracy" :chartOptions="chartOptionsAccuracy" />
                                        <ChartResult :key="componentKeyLoss" v-bind:chartData="chartDataLoss" :chartOptions="chartOptionsLoss" />
                                    </div>
                                </div>
                                <div class="text-center flex-fill d-flex flex-column">
                                    <h4 class="mb-3"><strong>Aggregated model results on test data for round {{this.session.federated_round - 1}}:</strong></h4>
                                    <div class="">
                                        <h4 class="mb-3 text-primary"> <strong>Accuracy: </strong></h4>
                                        <h4 class="mb-3"> <strong>{{this.globalModelAccuracy}} %</strong></h4>
                                    </div>
                                    <div class="">
                                        <h4 class="mb-3 text-danger"> <strong>Loss: </strong></h4>
                                        <h4 class="mb-3"> <strong>{{this.globalModelLoss}}</strong></h4>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-if="renderChart" class="row mt-3">
                            <div class="w-100 d-flex col mb-3 shadow p-3 mb-5  rounded" style="background-color: #f1f1f1;">
                                <div>
                                    <h4 class='mb-3'><strong>Global model accuracy and loss curves</strong></h4>
                                    <div class="d-flex justify-content-center">
                                        <LineChartResult :key="componentGlobalAccuracies" v-bind:chartData="globalAccuracies" :chartOptions="chartOptionsAccuracy" />
                                        <LineChartResult :key="componentGlobalLosses" v-bind:chartData="globalLosses" :chartOptions="chartOptionsLoss" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="tab-pane fade" id="nav-manageSession" role="tabpanel" aria-labelledby="nav-manageSession-tab">
                    <div class="row mt-3">
                        <div class="col mb-3 shadow p-3 mb-5 rounded" style="background-color: #f1f1f1;
                                   ">

                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col mb-3 shadow p-3 mb-5 d-flex justify-content-center rounded" style="background-color: #f1f1f1;">

                        </div>
                    </div>
                </div>

            </div>
            <div class="d-flex justify-content-between">
                <button class="btn btn-primary btn-lg btn-block" @click="backToSessions()">Back to sessions</button>
                <button v-if="session.founder != this.$store.state.user.username && !this.$store.state.isLoading" class="btn btn-danger btn-lg btn-block" @click="leaveSession()">Leave session</button>
                <button v-if="session.founder == this.$store.state.user.username" class="btn btn-lg btn-danger" @click="deleteSession()">Delete session</button>
            </div>
            <Loading />
        </div>
    </div>
</div>
</template>

<style>

</style>

<script>
// import participantJson from '@/participants.json'
import axios from 'axios'
//import Chart from '@/components/Chart.vue'
import ChartResult from '@/components/ChartResult.vue'
import Loading from '@/components/Loading.vue'
import LineChartResult from '@/components/LineChartResult.vue'

export default {
    components: {
        ChartResult,
        Loading,
        LineChartResult
    },
    beforeCreate() {
        //this.$options.components.ChartResult = require('@/components/ChartResult.vue').default;
    },
    data() {
        return {
            // participantList: participantJson,
            downloadingLocalAggregation: false,
            isActive: false,
            sessionEnded: false,
            downloadingScript: false,
            showStep1: true,
            showStep2: false,
            showStep3: false,
            showStep4: false,
            currentResult: {},
            debug: false,
            showResultsTab: false,
            data_for_chart: {},
            startDate: '2022-01-01',
            allWeightsUploaded: false,
            endDate: '2022-02-01',
            session: {},
            globalModelAccuracy: 0,
            globalModelLoss: 0,
            participants: [],
            aggregating: false,
            errors: [],
            data_path: '',
            renderChart: false,
            usernames: [],
            componentKey: 0,
            componentKeyLoss: 0,
            componentGlobalAccuracies: 0,
            componentGlobalLosses: 0,
            localLearningScriptDownloaded: false,
            localModelWeightUploaded: false,
            resultsFileUploaded: false,
            participantsProgress: [],
            globalAccuracies: {
                labels: ["1", "2", "3", "4", "5", "6", "7"], //response.data.names,
                datasets: [{
                    label: 'Learning rounds vs accuracy',
                    backgroundColor: 'rgb(77, 137, 255)',
                    data: [23, 36, 40, 45, 49, 51, 53] //response.data.accuracy
                }]
            },
            globalLosses: {
                labels: ["1", "2", "3", "4", "5", "6", "7"], //response.data.names,
                datasets: [{
                    label: 'Learning rounds vs loss',
                    backgroundColor: '#f87979',
                    data: [0.87, 0.83, 0.79, 0.65, 0.6, 0.55, 0.50] //response.data.accuracy
                }]
            },
            chartDataAccuracy: {
                labels: ["Hello"], //response.data.names,
                datasets: [{
                    label: 'Data One',
                    backgroundColor: '#f87979',
                    data: [1] //response.data.accuracy
                }]
            },
            chartDataLoss: {
                labels: ["Hello"], //response.data.names,
                datasets: [{
                    label: 'Data One',
                    backgroundColor: 'rgb(77, 137, 255)',
                    data: [1] //response.data.accuracy
                }]
            },
            chartOptionsAccuracy: {
                responsive: true,
                size: {

                    height: 25

                },
                scales: {
                    yAxes: [{
                        ticks: {
                            min: 0,
                            beginAtZero: true,
                            max: 100
                        }
                    }]
                }
            },
            chartOptionsLoss: {
                responsive: true,
                size: {

                    height: 25

                },
                scales: {
                    yAxes: [{
                        ticks: {
                            min: 0,
                            beginAtZero: true,
                            max: 1
                        }
                    }]
                }
            }
        }
    },
    async mounted() {
        this.$store.state.isLoading = true
        await axios.get('/api/v1/session/' + this.$route.params.id)
            .then(response => {
                this.session = response.data
                console.log(this.session)
                if (new Date(this.session.start_date) <= new Date(Date.now()) &&
                    this.session.actual_num_of_participants >= this.session.min_num_of_participants
                )
                    this.isActive = true

                if (this.session.end_date != null && new Date(this.session.end_date) <= new Date(Date.now())) {
                    this.isActive = false
                    this.sessionEnded = true
                }
            }).catch(error => {
                if (error.response) {
                    for (const property in error.response.data) {
                        this.errors.push(`${property}: ${error.response.data[property]}`)
                    }
                } else if (error.message) {
                    this.errors.push('Something went wrong. Please try again.')
                }
            })

        await axios.get('/api/v1/participants/session/' + this.$route.params.id).then(response => {
            this.participants = response.data
            console.log(this.participants)

        }).catch(error => {
            if (error.response) {
                for (const property in error.response.data) {
                    this.errors.push(`${property}: ${error.response.data[property]}`)
                }
            } else if (error.message) {
                this.errors.push('Something went wrong. Please try again.')
            }
        })

        for (const user in this.participants)
            this.usernames.push(user['username'])
        this.getParticipantsProgress()

    },
    methods: {
        getParamName(x) {
            const paramDic = {
                'number_of_epochs': "Number of epochs",
                'loss_function': "Loss function",
                'optimizer': "Optimizer",
                'learning_rate': "Learning rate",
                'momentum': "Momentum",
                'batch_size': "Batch size",
                'validation_split': "Validation split",
                'width_size': "Width size",
                'height_size': "Height size",
                'number_of_classes': "Number of classes",

            }
            return paramDic[x]
        },
        getRoundResults() {
            axios.get('/api/v1/get-round-results/' + this.$route.params.id)
                .then(response => {
                    console.log(response)
                    this.globalModelAccuracy = response.data.global_model_accuracy.toFixed(4) * 100
                    this.globalModelLoss = response.data.global_model_loss.toFixed(2)
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
        styleFounder(username) {
            if (username === this.session.founder) {
                return "background-color: #ffc34d;"
            }
        },
        getParticipantsProgress() {
            axios.get('/api/v1/participantstrainingprocess/' + this.$route.params.id)
                .then(response => {
                    this.participantsProgress = response.data
                    if (this.participantsProgress.every(x => x.is_model_uploaded)) {
                        this.showStep2 = false

                    } else {
                        this.showStep2 = true
                    }

                    axios.get('/api/v1/global-model-results/' + this.$route.params.id)
                        .then(response2 => {
                            let result = response2.data.find(elem => elem.federated_round == this.session.federated_round)
                            this.currentResult = result
                            if (result.finished == false) {
                                this.showStep3 = false
                                this.showStep4 = false
                            } else {
                                this.showStep3 = true
                            }

                            this.showResultsTab = response2.data.some(x => x.finished)
                            this.$store.state.isLoading = false

                        }).catch(error => {
                            if (error.response) {
                                for (const property in error.response.data) {
                                    this.errors.push(`${property}: ${error.response.data[property]}`)
                                }
                            } else if (error.message) {
                                this.errors.push('Something went wrong. Please try again.')
                            }
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
        forceRerender() {
            this.componentKey += 1
            this.componentKeyLoss += 1
            this.componentGlobalAccuracies += 1
            this.componentGlobalLosses += 1
        },
        fillData() {
            axios.get('/api/v1/results-for-chart/' + this.$route.params.id)
                .then(response => {
                    let accuracy = Array.from(response.data.accuracy, a => a.toFixed(4) * 100)

                    this.chartDataAccuracy = {
                        labels: response.data.names,
                        datasets: [{
                            label: 'Accuracy %',
                            backgroundColor: 'rgb(77, 137, 255)',
                            data: accuracy
                        }]
                    }
                    this.chartDataLoss = {
                        labels: response.data.names,
                        datasets: [{
                            label: 'Loss',
                            backgroundColor: '#f87979',
                            data: response.data.losses,
                        }]
                    }

                    axios.get('/api/v1/global-model-results/' + this.$route.params.id)
                        .then(response2 => {
                            console.log(response2)
                            let accuracies = Array.from(response2.data.filter(x => x.global_model_accuracy != null), a => a.global_model_accuracy.toFixed(4) * 100)
                            let losses = Array.from(response2.data.filter(x => x.global_model_accuracy != null), a => a.global_model_loss)
                            let labels = Array.from({
                                length: accuracies.length
                            }, (_, i) => i + 1)

                            this.globalAccuracies = {
                                labels: labels,
                                datasets: [{
                                    label: 'Rounds vs Accuracy %',
                                    backgroundColor: 'rgb(77, 137, 255)',
                                    data: accuracies
                                }]
                            }
                            this.globalLosses = {
                                labels: labels,
                                datasets: [{
                                    label: 'Rounds vs Loss',
                                    backgroundColor: '#f87979',
                                    data: losses,
                                }]
                            }
                            this.renderChart = true;
                            this.forceRerender()
                            this.getRoundResults()
                        }).catch(error => {
                            if (error.response) {
                                for (const property in error.response.data) {
                                    this.errors.push(`${property}: ${error.response.data[property]}`)
                                }
                            } else if (error.message) {
                                this.errors.push('Something went wrong. Please try again.')
                            }
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
        getRandomInt() {
            return Math.floor(Math.random() * (10 - 5 + 1)) + 10
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
            if (!confirm("Are you sure you would like to delete this session? This action cannot be undone."))
                return
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
            this.aggregating = true
            axios.get('/api/v1/aggregate-on-server/' + this.$route.params.id)
                .then(response => {
                    this.aggregating = false
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
                    this.resultsFileUploaded = true
                })
                .catch(function () {
                    console.log('FAILURE!!');
                })
        },
        getManyWeights() {
            axios({
                url: 'api/v1/get-local-weights/' + this.session.session_id,
                //url: 'api/v1/testmodel/',
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                console.log(response)
                var fileURL = window.URL.createObjectURL(new Blob([response.data], {
                    type: 'application/zip'
                }));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download', this.session.name + 'localweights.zip');
                document.body.appendChild(fileLink);

                fileLink.click();

                console.log(response)
                this.downloadTestDataset()
                this.downloadingLocalAggregation = false
            })

            // console.log(this.participants[0].username)
            // const array = this.participants; // changed the input array a bit so that the `array[i].id` would actually work - obviously the asker's true array is more than some contrived strings
            // let users = [];
            // let promises = [];
            // for (let i = 0; i < array.length; i++) {
            //     promises.push(

            //     )
            // }

            // Promise.all(promises).then(() => console.log(users));
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
                url: 'api/v1/get-local-weights/' + this.session.session_id,
                //url: 'api/v1/testmodel/',
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                console.log(response)
                var fileURL = window.URL.createObjectURL(new Blob([response.data], {
                    type: 'application/zip'
                }));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download', 'sessiongit.zip'); // 'file.pdf' do zmiany na rozszerzenie pliku ktory sie rzeczywiscie pobralo
                document.body.appendChild(fileLink);

                fileLink.click();

                console.log(response)
            })
        },
        downloadTestDataset() {
            axios({
                url: 'api/v1/download-zip-testdata/' + this.session.session_id,
                //url: 'api/v1/testmodel/',
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                console.log(response)
                var fileURL = window.URL.createObjectURL(new Blob([response.data], {
                    type: 'application/zip'
                }));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download', this.session.name + 'test_dataset.zip');
                document.body.appendChild(fileLink);

                fileLink.click();

                
            }).then(response2 =>{
                this.downloadingScript = false
            })
        },

        generateLocalModel() {
            if (!this.isActive)
                return
            this.downloadingScript = true
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
                this.showStep2 = true
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
                    this.downloadTestDataset()
                    this.localLearningScriptDownloaded = true
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
            this.downloadingLocalAggregation = true
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
                    this.getManyWeights()
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
                    this.uploadLocalWeights = true
                    this.getParticipantsProgress()
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
