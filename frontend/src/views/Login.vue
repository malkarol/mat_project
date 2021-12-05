<template>
      <div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
        <div class="card border-0 shadow rounded-3 my-5">
          <div class="card-body p-4 p-sm-5 mb-5">
            <h3 class="text-center">Login</h3>
             <hr />
            <form>
              <div class="form-floating mb-3">
                <input type="email" class="form-control" id="loginEmail" placeholder="name@example.com">
                <label for="floatingInput">Email address</label>
              </div>
              <div class="form-floating mb-3">
                <input type="password" class="form-control" id="loginPassword" placeholder="Password">
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
