<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">MAT</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
         <li class="nav-item">
          <router-link class="nav-link" to="/">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/">Getting started</router-link>
        </li>
        <li v-if="isLogged() === true" class="nav-item" >
          <router-link class="nav-link" to="/session">Create new session</router-link>
        </li>
        <li v-if="isLogged() === true" class="nav-item">
          <router-link class="nav-link" to="/sessions">Sessions</router-link>
        </li>

      </ul>
      <div v-if="isLogged() === false" class="collapse navbar-collapse justify-content-end"  >
      <ul  class="navbar-nav">
         <li  class="nav-item">
          <router-link class="nav-link " to="/login">Login</router-link>
        </li>
        <li  class="nav-item">
          <router-link class="nav-link " to="/register">Register</router-link>
        </li>
      </ul>
      </div>
       <div v-if="isLogged() === true" class="collapse navbar-collapse justify-content-end"  >
      <ul  class="navbar-nav">
         <li  class="nav-item">
          <button type="button" class="btn btn-primary navbar-btn" @click=logout()> Log out</button>
        </li>

      </ul>
      </div>
    </div>
  </div>
</nav>
</template>
<script>
import axios from 'axios'
export default {
  data () {
    return {

    }
  },

  methods: {
    async logout(){
      await axios
            .post('/api/v1/token/logout/')
            .then( response => {
              console.log('Logged out')
            })
            .catch(error => {
              console.log(JSON.stringify(error))
            })
            axios.defaults.headers.common['Authorization'] = ''
            localStorage.removeItem['token']
            this.$store.commit('removeToken')
            this.$router.push('/')
    },
    isLogged () {
      if (!this.$store.state.isAuthenticated)
      {
        return false
      }
      return true

    }
  }
}
</script>
