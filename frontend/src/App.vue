<template>
  <div>
    <NavBar />
    <div class="row">
        <router-view :sessions="sessions" />
    </div>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import sessionsJson from './sessions.json'

export default {
  name: 'App',
  components: {
    NavBar
  },
  data () {
    return {
      sessions: sessionsJson
    }
  }
}
</script>
