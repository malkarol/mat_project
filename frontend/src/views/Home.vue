<template>
  <div>
    <header class="py-5" style="background-color: #011f4b;">
      <div class="container-fluid px-5">
        <div class="row gx-5 justify-content-center">
          <div class="col-lg-6">
            <div class="text-center my-5">
              <h1 class="display-5 fw-bolder text-white mb-2">
                MAT - Model Aggregation Tool
              </h1>
              <p class="lead text-white-50 mb-4">
                A web platform for collaborative machine learning without centralized training data
              </p>
              <div class="d-grid gap-3 d-sm-flex justify-content-sm-center">
                <a class="btn btn-primary btn-lg px-4 me-sm-3" href="#features"
                  >Get Started</a
                >
                <a class="btn btn-outline-light btn-lg px-4" href="https://github.com/malkarol/mat_project">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="24" fill="currentColor" class="bi bi-github" viewBox="0 2 16 16">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                    GitHub</a
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
    <!-- Features section-->
    <section class="py-5 border-bottom" id="features">
            <div class="container px-5 my-5">
                <div class="row gx-5">
                    <div class="col-lg-4 mb-5 mb-lg-0">
                        <div class="feature bg-primary bg-gradient text-white rounded-3 mb-3"><i class="bi bi-collection"></i></div>
                        <h2 class="h4 fw-bolder">Federated learning</h2>
                        <p>Federated Learning is very new. As a part of Machine Learning it was introduce by Google to teach <strong>"cohorts"</strong> of edge devices. Now we present to you software that can allow you to grasp the idea of Federated Learning.</p>
                        <a class="text-decoration-none" href="https://venturebeat.com/2021/08/13/what-is-federated-learning/">
                            More about Federated Learning
                            <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                    <div class="col-lg-4 mb-5 mb-lg-0">
                        <div class="feature bg-primary bg-gradient text-white rounded-3 mb-3"><i class="bi bi-building"></i></div>
                        <h2 class="h4 fw-bolder">Free to use</h2>
                        <p>If you are not sure how to use <strong> MAT </strong> or you are just taking first steps with <strong> Machine Learning </strong> and <strong> Federated Learning </strong> you can start for free and ugrade your plan later.</p>

                    </div>
                    <div class="col-lg-4">
                        <div class="feature bg-primary bg-gradient text-white rounded-3 mb-3"><i class="bi bi-toggles2"></i></div>
                        <h2 class="h4 fw-bolder">No data sharing</h2>
                        <p>You do not have to worry about your data safety, <strong> MAT </strong> does not take your data for Federated Learning. You only upload trained weigths to the server, which minimizes chances of privacy breach.</p>

                    </div>
                </div>
            </div>
        </section>
        <!-- Pricing section-->
        <section class="bg-light py-5 border-bottom">
            <div class="container px-5">
                <div class="text-center mb-5">
                    <h2 class="fw-bolder">Pay to learn faster grow</h2>
                    <p class="lead mb-0">With our fantastic pricing plans</p>
                </div>
                <div class="row gx-5 justify-content-center">
                    <!-- Pricing card free-->
                    <div class="col-lg-6 col-xl-4">
                        <div class="card mb-5 mb-xl-0">
                            <div class="card-body p-5">
                                <div class="small text-uppercase fw-bold text-muted">Free</div>
                                <div class="mb-3">
                                    <span class="display-4 fw-bold">$0</span>

                                </div>
                                <ul class="list-unstyled mb-4">
                                    <li class="mb-2">
                                        <i class="bi bi-check text-primary"></i>
                                        <strong>Limited access</strong>
                                    </li>
                                    <li class="mb-2">
                                        <i class="bi bi-check text-primary"></i>
                                        Access to only public sessions
                                    </li>
                                    <li class="mb-2">
                                        <i class="bi bi-check text-primary"></i>
                                        Client-side aggregation
                                    </li>
                                    <li class="mb-2">
                                        <i class="bi bi-check text-primary"></i>
                                        More user interaction required
                                    </li>
                                    <li class="mb-2">
                                        <i class="bi bi-x"></i>
                                        Less automated learning
                                    </li>
                                    <li class="mb-2 ">
                                        <i class="bi bi-x"></i>
                                        Sessions access restriction
                                    </li>
                                </ul>
                                <div class="d-grid"><a class="btn btn-primary" @click="this.$router.push({ path: 'register', query: { plan: 'free' } })">Choose plan</a></div>
                            </div>
                        </div>
                    </div>
                    <!-- Pricing card pro-->
                    <div class="col-lg-6 col-xl-4">
                        <div class="card mb-5 mb-xl-0">
                            <div class="card-body p-5">
                                <div class="small text-uppercase fw-bold">
                                    &#11088;
                                    Premium
                                </div>
                                <div class="mb-3">
                                    <span class="display-4 fw-bold">$3</span>

                                </div>
                                <ul class="list-unstyled mb-4">
                                    <li class="mb-2">
                                        <i class="bi bi-check text-primary"></i>
                                        <strong>Unlimited access</strong>
                                    </li>
                                    <li class="mb-2">
                                        <i class="bi bi-check text-primary"></i>
                                        Access to public sessions
                                    </li>
                                    <li class="mb-2">
                                        <i class="bi bi-check text-primary"></i>
                                        Access to private sessions
                                    </li>
                                    <li class="mb-2">
                                        <i class="bi bi-check text-primary"></i>
                                        Server-side aggregation
                                    </li>
                                    <li class="mb-2">
                                        <i class="bi bi-check text-primary"></i>
                                        More automated learning
                                    </li>
                                    <li class="mb-2">
                                        <i class="bi bi-check text-primary"></i>
                                        Dedicated support
                                    </li>
                                </ul>
                                <div class="d-grid"><a @click="this.$router.push({ path: 'register', query: { plan: 'premium' } })" class="btn btn-primary">Choose plan</a></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
  </div>
</template>
