<template>
  <div class="Site">
    <NavBar />
    <div class="row Site-content">
        <router-view />
    </div>
    <Footer />
  </div>

</template>

<script>
import axios from 'axios'
import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'
export default {
  name: 'App',
  components: {
    NavBar,
    Footer
  },
  beforeCreate () {
    this.$store.commit('initializeStore')

    if (this.$store.state.token) {
      axios.defaults.headers.common['Authorization'] = 'Token ' + this.$store.state.token
    } else {
      axios.defaults.headers.common['Authorization'] = ''
    }
  }

}
</script>
<style>
.Site {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

.Site-content {
  flex: 1;
}
</style>
