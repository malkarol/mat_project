<template>
  <div class="row">
    <div class="col-md-6 offset-md-3">
      <div>
        <div>
          <h3>Registration</h3>
          <hr />
        </div>
       <form class="row g-4">
  <div class="col-md-6">
    <label for="inputUserName" class="form-label">User name</label>
    <input type="text" class="form-control" id="inputUserName">
  </div>
   <div class="col-md-6">
    <label for="inputFullName" class="form-label">Full Name</label>
    <input type="text" class="form-control" id="inputFullName">
  </div>
   <div class="col-md-6">
    <label for="inputEmail" class="form-label">Email</label>
    <input type="email" class="form-control" id="inputEmail">
  </div>
  <div class="col-md-6">
    <label for="inputEmailConfirm" class="form-label">Repeat email</label>
    <input type="email" class="form-control" id="inputEmailConfirm">
  </div>
  <div class="col-md-6">
    <label for="inputPassword" class="form-label">Password</label>
    <input type="password" class="form-control" id="inputPassword">
  </div>
   <div class="col-md-6">
    <label for="inputPasswordConfirm" class="form-label"> Repeat password</label>
    <input type="password" class="form-control" id="inputPasswordConfirm">
  </div>
  <div class="col-md-12"><small id="passwordHelpBlock" class="form-text text-muted">
  Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.
</small></div>
  <div class="col-md-6">
    <label for="inputState" class="form-label">Machine Learning background</label>
    <select id="inputState" class="form-select">
      <option selected>Choose...</option>
      <option value="1">Student</option>
      <option value="2">Professor</option>
      <option value="3">Professional</option>
      <option value="4">Hobbyst</option>
    </select>
  </div>
  <div class="col-md-6">
    <label for="inputState" class="form-label">Pricing Plan</label>
    <select id="inputState" class="form-select">
      <option value="1" selected>Free</option>
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
                    />
                    <label class="form-check-label" for="form2Example3">
                      I agree all statements in <a href="#!">Terms of service</a>
                    </label>
                  </div>
  </div>
  <div class="col-12">
    <button type="submit" class="btn btn-primary">Register</button>
  </div>
</form>
      </div>
    </div>
  </div>
</template>
