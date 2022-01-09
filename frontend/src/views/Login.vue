<template>
      <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
        <div v-if="errors.length" class="alert alert-danger d-flex align-items-center" role="alert" >
          <svg  class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
          <div v-for="error in errors" v-bind:key="error" >
            {{ error }}
          </div>
        </div>
        <div class="card border-0 shadow rounded-3 my-5">
          <div class="card-body p-4 p-sm-5 mb-5">
            <h3 class="text-center">Login</h3>
             <hr />
            <form @submit.prevent="submitForm">
              <div class="form-floating mb-3">
                <input type="email" class="form-control" id="loginEmail" placeholder="name@example.com" v-model="email">
                <label for="floatingInput">Email address</label>
              </div>
              <div class="form-floating mb-3">
                <input type="password" class="form-control" id="loginPassword" placeholder="Password" v-model="password">
                <label for="floatingPassword">Password</label>
              </div>

              <div class="form-check mb-3">
                <input class="form-check-input" type="checkbox" value="" id="rememberPasswordCheck">
                <label class="form-check-label" for="rememberPasswordCheck">
                  Remember my password
                </label>
              </div>
              <div class="d-grid">
                <button class="btn btn-primary" type="submit">Login</button>
              </div>
              <hr class="my-4">
            </form>
          </div>
        </div>
      </div>
</template>
<script>
import axios from 'axios'
export default {
  data () {
    return {
      password: '',
      email: '',
      errors: []
    }
  },
  methods: {
    async submitForm () {
      this.$store.commit('setIsLoading', true)
      axios.defaults.headers.common['Authorization'] = ''
      localStorage.removeItem('token')

      const formData = {
        email: this.email,
        password: this.password
      }

      await axios
          .post('/api/v1/token/login', formData)
          .then(response => {
            const token = response.data.auth_token

            this.$store.commit('setToken', token)

            axios.defaults.headers.common['Authorization'] = 'Token ' + token

            localStorage.setItem('token', token)



          })
          .catch( error => {
            if (error.response) {
              for (const property in error.response.data){
                this.errors.push(`${property}: ${error.response.data[property]}`)
              }
            } else if (error.message){
              this.errors.push('Something went wrong. Please try again.')
            }
          })

          await axios
                .get('/api/v1/users/me/')
                .then( response => {
                  console.log(response)
                  this.$store.commit('setUser', { 'id': response.data.id, 'username': response.data.username, 'pricing_plan': response.data.pricing_plan})

                  localStorage.setItem('username', response.data.username)
                  localStorage.setItem('userid', response.data.id)
                  localStorage.setItem('pricing_plan', response.data.pricing_plan)

                  this.$router.push('/sessions')
                })
                .catch( error =>
                {
                  console.log(error )
                })

        this.$store.commit('setIsLoading', false)

    }
  }
}
</script>