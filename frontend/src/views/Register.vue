<template>
<div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
        <div class="card border-0 shadow rounded-3 my-5">
          <div class="card-body p-4 p-sm-5 mb-5">
        <div>
          <h3>Registration</h3>
          <hr />
        </div>
        <form
          class="row g-3 needs-validation"
          oninput='inputPasswordConfirm.setCustomValidity(inputPasswordConfirm.value != inputPassword.value ? "Passwords do not match." : "");
      inputEmailConfirm.setCustomValidity(inputEmailConfirm.value != inputEmail.value ? "Passwords do not match." : "");'
          novalidate
        >
          <div class="col-md-6 position-relative">
            <label for="inputUserName" class="form-label">User name</label>
            <input
              type="text"
              class="form-control"
              id="inputUserName"
              required
            />
          </div>
          <div class="col-md-6 has-validation">
            <label for="inputFullName" class="form-label">Full Name</label>
            <input
              type="text"
              class="form-control"
              id="inputFullName"
              required
            />
          </div>
          <div class="col-md-6">
            <label for="inputEmail" class="form-label">Email</label>
            <input type="email" class="form-control" id="inputEmail" required />
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
            <select id="inputState" class="form-select" required>
              <option value="" selected disabled hidden>Choose...</option>
              <option value="1">Student</option>
              <option value="2">Professor</option>
              <option value="3">Professional</option>
              <option value="4">Hobbyst</option>
            </select>
          </div>
          <div class="col-md-6">
            <label for="inputState" class="form-label">Pricing Plan</label>
            <select id="inputState" class="form-select" required>
              <option value="" selected disabled hidden>...</option>
              <option value="1">Free</option>
              <option value="2">Premium</option>
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
export default {
  methods: {
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
