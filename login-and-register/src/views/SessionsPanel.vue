<template>
    <div>
      Sessions Panel
      <div v-for="(session) in sessions.slice(0,3)" :key="session.id" >
         <div>
            {{session.name}}
            <hr/>
          </div>
      </div>
    </div>
</template>
<script>
export default {
  props: ['sessions']
}
</script>
