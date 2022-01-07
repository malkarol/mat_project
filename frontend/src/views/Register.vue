<template>
<div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
  <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
  <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
  </symbol>
  <symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16">
    <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
  </symbol>
</svg>
    <div  v-if="isModalVisible" class="alert alert-success d-flex align-items-center  alert-dismissible" role="alert">
  <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
  <div>
    Account was created, please log in.
  </div>
  <button @click="toggleModalAlert()" type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
<div v-if="errors.length" class="alert alert-danger d-flex align-items-center" role="alert" >
  <svg  class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
  <div v-for="error in errors" v-bind:key="error" >
    {{ error }}
  </div>
</div>
        <div class="card border-0 shadow rounded-3 my-5">
          <div class="card-body p-4 p-sm-5 mb-5">
        <div>
          <h3>Registration</h3>
          <hr />
        </div>
        <form @submit.prevent="submitForm"
          class="row g-3 needs-validation"
          oninput='inputPasswordConfirm.setCustomValidity(inputPasswordConfirm.value != inputPassword.value ? "Passwords do not match." : "");
      inputEmailConfirm.setCustomValidity(inputEmailConfirm.value != inputEmail.value ? "Passwords do not match." : "");'
          novalidate
        >
          <div class="col-md-6 position-relative">
            <label for="inputUserName" class="form-label" >User name</label>
            <input
              type="text"
              class="form-control"
              id="inputUserName"
              v-model="username"
              required
            />
          </div>
          <div class="col-md-6 has-validation">
            <label for="inputFullName" class="form-label">Full Name</label>
            <input
              type="text"
              class="form-control"
              id="inputFullName"
              v-model="fullName"
              required
            />
          </div>
          <div class="col-md-6">
            <label for="inputEmail" class="form-label">Email</label>
            <input type="email" class="form-control" id="inputEmail" v-model="email" required />
          </div>
          <div class="col-md-6">
            <label for="inputEmailConfirm" class="form-label"
              >Repeat email</label
            >
            <input
              type="email"
              class="form-control"
              id="inputEmailConfirm"
              required
            />
          </div>
          <div class="col-md-6">
            <label for="inputPassword" class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              id="inputPassword"
              v-model="password"
              required
            />
          </div>
          <div class="col-md-6">
            <label for="inputPasswordConfirm" class="form-label">
              Repeat password</label
            >
            <input
              type="password"
              class="form-control"
              id="inputPasswordConfirm"
              required
            />
            <div class="invalid-feedback">Passwords do not match</div>
          </div>
          <div class="col-md-12">
            <small id="passwordHelpBlock" class="form-text text-muted">
              Your password must be 8-20 characters long, contain letters and
              numbers, and must not contain spaces, special characters, or
              emoji.
            </small>
          </div>
          <div class="col-md-6">
            <label for="inputState" class="form-label"
              >Machine Learning background</label
            >
            <select id="inputState" class="form-select" required v-model="mlBackground">
              <option value="" selected disabled hidden>Choose...</option>
              <option value="0">Student</option>
              <option value="1">Professor</option>
              <option value="2">Professional</option>
              <option value="3">Hobbyst</option>
            </select>
          </div>
          <div class="col-md-6">
            <label for="inputState" class="form-label">Pricing Plan</label>
            <select id="inputState" class="form-select" required v-model="pricingPlan">
              <option value="" selected disabled hidden>...</option>
              <option value="0">Free</option>
              <option value="1">Premium</option>
            </select>
          </div>
          <div class="col-12">
            <div class="form-check d-flex justify-content-center mb-5">
              <input
                class="form-check-input me-2"
                type="checkbox"
                value=""
                id="form2Example3c"
                required
              />
              <label class="form-check-label" for="form2Example3">
                I agree all statements in <a href="#!">Terms of service</a>
              </label>
            </div>
          </div>
          <div class="col-12">
            <button
              type="submit"
              class="btn btn-primary"
              @click="validateForm()"
            >
              Register
            </button>
          </div>
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
      isModalVisible: false,
      username: '',
      password: '',
      email: '',
      fullName: '',
      pricingPlan: '',
      mlBackground: '',
      errors: []
    }
  },
  methods: {
    sleep (miliseconds) {
    var currentTime = new Date().getTime();

    while (currentTime + miliseconds >= new Date().getTime()) {
      }
    },
    canISeeModel () {
      return this.isModalVisible
    },
    toggleModalAlert () {
      console.log("hej")
      this.isModalVisible = false
    },
    async submitForm () {
      this.errors = []
      console.log('Sign up')
      console.log(this.username)
      console.log(this.password)
      console.log(this.email)
      console.log(this.fullName)
      console.log(this.pricingPlan)
      console.log(this.mlBackground)

      const formData = {
        username: this.username,
        password: this.password,
        email: this.email,
        first_name: this.fullName.split(' ').slice(0, -1).join(' '),
        last_name: this.fullName.split(' ').slice(-1).join(' ')
        // pricingPlan: this.pricingPlan,
        // mlBackgroun: this.mlBackground
      }
      this.$store.commit('setIsLoading', true)
      await axios
          .post('/api/v1/users/', formData)
          .then(response => {
            this.isModalVisible = true
            // toast({
            //   message: 'Account was created, please log in.',
            //   type: 'is-success',
            //   dissmissible: true,
            //   pauseOnHover: true,
            //   duration: 2000,
            //   position: 'bottom-right'
            // })
            this.sleep (3000)
            this.$router.push('/login')
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
          this.$$store.commit('setIsLoading', false)
    },
    validateForm () {
      'use strict'

      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.querySelectorAll('.needs-validation')

      // Loop over them and prevent submission
      Array.prototype.slice.call(forms).forEach(function (form) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      })
    },

    validatePassword () {

    },

    validateEmail () {

    }
  }
}
</script>
