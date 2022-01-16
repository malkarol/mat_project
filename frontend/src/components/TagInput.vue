<template>
  <div class="tag-input">
    <div v-for="(tag, index) in tags" :key="tag" class="tag-input__tag">
      <span @click="removeTag(index)">x</span>
      {{ tag }}
    </div>
   <input
      type='text'
      :placeholder="showName(name)"
      class='tag-input__text'
      @keydown='addTag'
      @keydown.delete="removeLastTag"
      :disabled ="disabled"

/>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        disabled: false,
      }
    },
    props:
    {
      filteredSessions:{
        type: Array,
        default: () => []
      },
      tags:{
        type: Array,
        default: () => []
      },
      maxInput:{
        type:Number,
        default: 10
      },
      isUsers:{
        type:Boolean,
        default: false
      },
      name:{
        type:String,
        default: "tags"
      }
    },
    emits: ["filterSessions"],
    methods: {
      addTag (event) {

        if(this.tags.length != this.maxInput)
        {
          if(event.code == 'Comma' || event.code == 'Enter' )
        {
          event.preventDefault()
          var val = event.target.value.trim()

          if (val.length > 0 && !this.tags.includes(val) && this.isOwner(val,this.isUsers)===false) {
            this.tags.push(val)
            this.$emit("filterSessions", "someValue");
            event.target.value = ''
          }
          console.log(this.tags)
        }

        }
      },
      isOwner (name,isUser){
        console.log(this.$store.state.user.username)
        if(isUser){
          if(name === this.$store.state.user.username)
          {
            return true
          }
          return false
        }
        else{
          return false
        }
      },
      removeTag (index){
        this.tags.splice(index,1)
        this.$emit("filterSessions", "someValue");
        console.log(this.tags)
      },
      removeLastTag (event) {
        if (event.target.value.length === 0)
        {
          this.removeTag(this.tags.length - 1)
          this.$emit("filterSessions", "someValue");
        }
         console.log(this.tags)
      },
      showName(name)
      {
        return "Enter " + name
      },


    }
  }
</script>
<style scoped>
  .tag-input {
    width: 100%;
    border: 1px solid #eee;
    font-size: 0.9em;
    height: 50px;
    box-sizing: border-box;
    padding: 0 10px;
  }

  .tag-input__tag {
    height: 30px;
    float: left;
    margin-right: 10px;
    background-color: #eee;
    margin-top: 10px;
    line-height: 30px;
    padding: 0 5px;
    border-radius: 5px;
  }

  .tag-input__tag > span {
    cursor: pointer;
    opacity: 0.75;
  }

  .tag-input__text {
    border: none;
    outline: none;
    font-size: 0.9em;
    line-height: 50px;
    background: none;
  }
</style>
