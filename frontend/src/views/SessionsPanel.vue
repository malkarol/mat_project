<template>
<div>
  <div class="container mt-3 py-5">
    <h2>Sessions</h2>
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
    <div  class="list-group">

      <div v-for="(session, index) in sortedList" class="border border-5" :key="session.name" data-bs-toggle="collapse" :data-bs-target="'#example_' + index" aria-expanded="false" :aria-controls="'example_' + index"
      v-bind:sortedList="sortedList">
         <div class="list-group-item list-group-item-action" :class="{'bg-primary text-white':index == selected}" @click="selected = index">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">{{session.name}} <span class="badge "
      :class="badgeColor(session.private)">{{badgeText(session.private)}}</span></h5>
      <small :class="textMutedColor(index)">3 days ago</small>
    </div>
    <p class="mb-1">Some placeholder content in a paragraph blank blan </p>
    <small :class="textMutedColor(index)">{{session.numberOfUsers}}/{{session.maxNumberOfUsers}} Users</small>
      <div class="collapse" :id="'example_' + index">
      <div class="card card-body border-0 text-black">
      <div class="container border rounded ">
        <div class="d-flex flex-row pt-2 border-bottom">
          <div class="p-2">
            <h5 class="mb-1">Details</h5>
          </div>
          <div class="p-2">
            <p v-if="Math.random() > 0.6"
            class="mb-1 text-success">Joined</p>
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
                <span class="">Karol</span>
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
          <button v-if="session.canJoin && session.maxNumberOfUsers > session.numberOfUsers"
          @click="router.push({ name: 'session', params: { sessionName: 'test' } })" class="btn btn-primary">Join session</button>

      </div>
    </div>
  </div>
  </div>
      </div>
        </div>

      </div>

    </div>
    <nav aria-label="...">
  <ul class="pagination">
    <li class="page-item">
      <a class="page-link" @click="prevPage" >Previous</a>
    </li>
    <li class="page-item">
      <a class="page-link" @click="nextPage">Next</a>
    </li>
  </ul>
</nav>
</div>
</div>
</template>
<script>
import sessionsJson from '@/sessions.json'

export default {
  data () {
    return {
      selected: undefined,
      search: '',
      sessions: sessionsJson,
      pageSize: 10,
      currentPage: 1
    }
  },
  methods: {
    badgeColor (value) {
      return {
        'bg-danger': value,
        'bg-success': !value
      }
    },
    badgeText (value) {
      if (value) {
        return 'Private'
      }
      return 'Public'
    },
    textMutedColor (value) {
      if (value === this.selected) {
        return 'text-white'
      }
      return 'text-muted'
    },
    nextPage () {
      if ((this.currentPage * this.pageSize) < this.filteredList.length) this.currentPage++
    },
    prevPage () {
      if (this.currentPage > 1) this.currentPage--
    }
  },
  watch: {
    search () {
      console.log('reset to p1 due to filter')
      this.currentPage = 1
    }
  },
  computed: {
    filteredList () {
      return this.sessions.filter(session => {
        return session.name.toLowerCase().includes(this.search.toLowerCase())
      })
    },
    sortedList () {
      return this.filteredList.filter((row, index) => {
        const start = (this.currentPage - 1) * this.pageSize
        const end = this.currentPage * this.pageSize
        if (index >= start && index < end) return true
      })
    },
    goToNewSessionView () {
      this.$router.push('/session')
    }
  }
}
</script>
