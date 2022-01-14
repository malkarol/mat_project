<template>
<div>
    <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #4d89ff;">
    <a class="navbar-brand " style="
    margin-right: 16px;
    margin-left: 16px;" href="#">
    <img src="@/assets/logo.png" width="30" height="30" alt="">
  </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
         <li class="nav-item">
          <router-link class="nav-link" to="/" style="text-decoration: none; color: inherit;" >Home</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/getting-started" style="text-decoration: none; color: inherit;">Getting started</router-link>
        </li>
        <!-- <li v-if="isLogged() === true"  class="nav-item">
          <router-link class="nav-link" to="/session" style="text-decoration: none; color: inherit;">SingleSession[Preview]</router-link>
        </li> -->
        <li v-if="isLogged() === true"  class="nav-item">
          <router-link class="nav-link" to="/sessions" style="text-decoration: none; color: inherit;">Sessions</router-link>
        </li>
        <li v-if="isLogged() === true"  class="nav-item">
          <router-link class="nav-link" to="/profile" style="text-decoration: none; color: inherit;">Profile</router-link>
        </li>
      </ul>

      <div v-if="isLogged() === false" class="collapse navbar-collapse justify-content-end"  >
      <ul  class="navbar-nav">
         <li  class="nav-item">
          <router-link class="nav-link " to="/login" style="text-decoration: none; color: inherit;">Login</router-link>
        </li>
        <li  class="nav-item">
          <router-link class="nav-link " to="/register" style="text-decoration: none; color: inherit;">Register</router-link>
        </li>
      </ul>
      </div>
       <div v-if="isLogged() === true" class="collapse navbar-collapse justify-content-end"  >
      <ul  class="navbar-nav">
         <li  class="nav-item">
          <button type="button" class="btn navbar-btn" style="text-decoration: none; color: inherit; background-color: #4d89ff;" @click=logout()> Log out</button>
        </li>

      </ul>
      </div>
    </div>
</nav>
</div>
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
            localStorage.removeItem('token')
            localStorage.removeItem('username')
            localStorage.removeItem('userid')
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
