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
        <li class="nav-item">
          <router-link class="nav-link" to="/session">SingleSession[Preview]</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/sessions">Sessions</router-link>
        </li>

      </ul>
      <div class="collapse navbar-collapse justify-content-end"  >
      <ul class="navbar-nav">
         <li class="nav-item">
          <router-link class="nav-link " to="/login">Login</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link " to="/register">Register</router-link>
        </li>
      </ul>
      </div>
    </div>
  </div>
</nav>
</template>
<script>
export default {
}
</script>
