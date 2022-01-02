<template>
  <div class="d-flex flex-column h-100">
    <NavBar />
    <div class="row flex-shrink-0">
        <router-view />
    </div>
    <Footer class="footer mt-auto py-3 bg-light"/>
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


</style>
