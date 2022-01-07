<template>
<div class="col-lg-10 mx-auto">
    <div class="card border-0 shadow rounded-3 my-5">
        <div class="card-body p-4 p-sm-5 mb-5">
            <div>
                <h2>Sessions</h2>
                <hr />
            </div>

            <p>Type something in the input field to search the list for specific items:</p>
            <div class="d-flex justify-content-between">
                <div class="col-sm-6"><input class="form-control" v-model="search" type="text" placeholder="Search..."></div>
                <div> <button type="button" class="btn btn-success" @click='goToNewSessionView'>
                        <!-- <router-link
    style="text-decoration: none; color: inherit;"
    to="/session"
    >Create session
    </router-link> -->
                        Create new session
                    </button>
                </div>
            </div>
            <br>
            <div class="list-group" style="min-height: 1150px">

                <div  v-for="(session, index) in sortedList" class="border border-5" :key="session.name" data-bs-toggle="collapse" :data-bs-target="'#example_' + index" aria-expanded="false" :aria-controls="'example_' + index" v-bind:sortedList="sortedList">
                    <div class="list-group-item list-group-item-action" :class="{'bg-primary text-white':index == selected}" @click="selected = index">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">{{session.name}} <span class="badge " :class="badgeColor(session.pricing_plan)">{{badgeText(session.pricing_plan)}}</span></h5>
                            <small :class="textMutedColor(index)">{{getDays(session.creation_date)}} days ago</small>
                        </div>
                        <p class="mb-1">{{session.description}}</p>
                        <small :class="textMutedColor(index)">{{session.actual_num_of_participants}}/{{session.max_num_of_participants}} Users</small>
                        <div class="collapse" :id="'example_' + index">
                            <div class="card card-body border-0 text-black">
                                <div class="container border rounded ">
                                    <div class="d-flex flex-row pt-2 border-bottom">
                                        <div class="p-2">
                                            <h5 class="mb-1">Details</h5>
                                        </div>
                                        <div class="p-2">
                                            <p v-if="isJoined(session.session_id) === true" class="mb-1 text-success">Joined</p>
                                            <p v-else class="mb-1 text-primary">Eligible to join</p>
                                        </div>
                                    </div>
                                    <div class="container py-2">
                                        <div class="row justify-content-start pt-3">
                                            <div class="col-3">
                                                <div class="row">
                                                    <label><strong>Founder</strong></label>
                                                </div>
                                            </div>
                                            <div class="col-6">
                                                <div class="row">
                                                    <span class="">{{session.founder}}</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row justify-content-start py-3">
                                            <div class="col-3">
                                                <div class="row">
                                                    <label><strong>Classification problem</strong></label>
                                                </div>
                                            </div>
                                            <div class="col-6">
                                                <div class="row">
                                                    <span class="">Image</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <div class="row">
                                        <div class="pt-3">
                                             <button v-if="isJoined(session.session_id)"
                                             @click="this.$router.push({ name: 'Session', params: { id: session.session_id } })"
                                             class="btn btn-primary">Go to session</button>
                                            <button v-else-if="session.max_num_of_participants > session.actual_num_of_participants"
                                             @click="joinSessionClicked(session.session_id)"
                                             class="btn btn-primary">Join session</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

            </div>
            <nav class="mt-2" aria-label="...">
                <ul class="pagination">
                    <li class="page-item">
                        <a class="page-link" @click="prevPage">Previous</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" @click="nextPage">Next</a>
                    </li>
                </ul>
            </nav>
            <button><a href="#">Button Text</a></button>
        </div>
    </div>
</div>
</template>

<script>
// import sessionsJson from '@/sessions.json'
import axios from 'axios'

export default {
    data() {
        return {
            selected: undefined,
            search: '',
            sessions:[],
            joinedSessions:[],
            pageSize: 10,
            currentPage: 1,
            isFetching: true
        }
    },
    mounted() {
        axios.get('/api/v1/sessions/').then(response => {
            this.sessions = response.data

        }).catch( error => {
            if (error.response) {
              for (const property in error.response.data){
                this.errors.push(`${property}: ${error.response.data[property]}`)
              }
            } else if (error.message){
              this.errors.push('Something went wrong. Please try again.')
            }
          }),
        axios
          .get('/api/v1/participants/filter/' + this.$store.state.user.id)
          .then(response => {
            this.joinedSessions = response.data
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
    methods: {
        badgeColor(value) {
            return {
                'bg-danger': value,
                'bg-success': !value
            }
        },
        badgeText(value) {
            if (value) {
                return 'Private'
            }
            return 'Public'
        },
        textMutedColor(value) {
            if (value === this.selected) {
                return 'text-white'
            }
            return 'text-muted'
        },
        nextPage() {
            if ((this.currentPage * this.pageSize) < this.filteredList.length) this.currentPage++
        },
        prevPage() {
            if (this.currentPage > 1) this.currentPage--
        },
        getDays(creationDate){
          const today = new Date()
          let creation_date = new Date(creationDate)
          let timeDiff = today.getTime() - creation_date.getTime()
          return Math.round(timeDiff / (1000 * 3600 * 24))
        },
        getJoinedSessions(){
          axios
          .get('/api/v1/participants/filter/' + this.$store.state.user.id)
          .then(response => {
            this.joinedSessions = response.data
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
        getFounderName(session){
          axios.get('/api/v1/participant/' + session.founder).then(resp => {
            console.log(resp.data)
            axios.get('/user/' + resp.data.user).then(response =>{
              return response.data.username
            })
        })
        },
        isJoined(session_id){
            return this.joinedSessions.includes(session_id)
        },
        async joinSessionClicked(session_id){

            const formData = {
                session_id: session_id,
                new_participant: this.state.user.id
            }
            await axios
          .post('/api/v1/session/add-participant/', formData)
          .then(response => {

            this.$router.push({ name: 'Session', params: { id: session.session_id } })


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

        },
        addNumberOfCurrentParticipants(session_id){

        }
    },
    watch: {
        search() {
            console.log('reset to p1 due to filter')
            this.currentPage = 1
        }
    },
    computed: {
        filteredList() {
            return this.sessions.filter(session => {
                return session.name == null ? "" : session.name.toLowerCase().includes(this.search.toLowerCase())
            })
        },
        sortedList() {
            return this.filteredList.filter((row, index) => {
                const start = (this.currentPage - 1) * this.pageSize
                const end = this.currentPage * this.pageSize
                if (index >= start && index < end) return true
            })
        },
        goToNewSessionView() {
            this.$router.push('/new-session')
        }
    }
}
</script>
