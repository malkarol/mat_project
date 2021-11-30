<template>
<div>
  <div class="py-5">
    <div  class="list-group">

      <div v-for="(session, index) in sessions.slice(0,10)" class="border border-5" :key="session.name" data-bs-toggle="collapse" :data-bs-target="'#example_' + index" aria-expanded="false" :aria-controls="'example_' + index">
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
          <br>
    Some placeholder content in a paragraph <br>
    Some placeholder content in a paragraph <br>
      Some placeholder content in a paragraph <br>
    Some placeholder content in a paragraph <br>
      Some placeholder content in a paragraph <br>
    Some placeholder content in a paragraph <br>
  </div>
      </div>
        </div>

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
</div>
</template>
<script>
export default {
  props: ['sessions'],
  data () {
    return {
      selected: undefined
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
    }
  }
}
</script>
