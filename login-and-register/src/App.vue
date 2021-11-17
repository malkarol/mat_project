<template>
<div>
  <NavBar/>
  <div class="container">
    <div class="row">
      <div class="col-md-12 pt-5">
        <div>
          <router-view/>
        </div>
      </div>
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
