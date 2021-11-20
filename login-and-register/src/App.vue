<template>
  <div>
    <NavBar />
    <div class="container-fluid g-0">
      <div class="row">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components: {
    NavBar
  }
}
</script>
