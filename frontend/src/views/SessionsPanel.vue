<template>
<div>
    <div  class="list-group">

      <div v-for="(session) in sessions.slice(0,10)" :key="session.id" >
         <router-link to="/" class="list-group-item list-group-item-action">
    <div class="d-flex w-100 justify-content-between">
      <h5 class="mb-1">{{session.name}} <span class="badge "
      :class="badgeColor(session.Private)">{{badgeText(session.Private)}}</span></h5>
      <small class="text-muted">3 days ago</small>
    </div>
    <p class="mb-1">Some placeholder content in a paragraph blank blan </p>
    <small class="text-muted">{{session.numberOfUsers}}/{{session.maxNumberOfUsers}} Users</small>
         </router-link>

      </div>
    </div>
    <nav aria-label="...">
  <ul class="pagination">
    <li class="page-item disabled">
      <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Previous</a>
    </li>
    <li class="page-item"><a class="page-link" href="#">1</a></li>
    <li class="page-item active" aria-current="page">
      <a class="page-link" href="#">2</a>
    </li>
    <li class="page-item"><a class="page-link" href="#">3</a></li>
    <li class="page-item">
      <a class="page-link" href="#">Next</a>
    </li>
  </ul>
</nav>
</div>
</template>
<script>
export default {
  props: ['sessions'],
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
    }
  }
}
</script>
