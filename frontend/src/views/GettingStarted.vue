<template>
<div class="col-lg-10 mx-auto w-50">
    <div class="card border-0 shadow rounded-3 my-5">
        <div class="card-body p-4 p-sm-5 mb-5">
            <div>
                <h2>Getting started</h2>
                <hr />
            </div>
            <section class="mt-5">
                <div>
                    <h4>Overview</h4>
                </div>
                <p>
                    The following document allows you to understand how our software works and how to use.
                    <br> Despite our best efforts, please be patient during running Machine Learning scripts
                    <br>and remeber that some error and issues might be not handled.
                </p>
                <hr>
                <div>
                    <h4>Prerequisites</h4>
                </div>
                <p>In order to use <strong>M</strong>odel <strong>A</strong>ggregation <strong>T</strong>ool webpage you don't have to have anything installed.
                <br>However, in order to use Python scripts on your PC it is adviced that you have <strong>Python 3.7+</strong> and <strong>Tensorflow 2</strong> installed.
                <br>If you don't have them please go to the following web pages, download them and use tutorials for installation.
                    </p>
                    <ul>
                        <li><a href="https://www.python.org/downloads/">Python</a> </li>
                        <li><a href="https://www.tensorflow.org/install">Tensorflow</a></li>

                    </ul>

                <p class="text-danger"> Currently, only Windows architecture is supported for execution  of ELL and ALL desktop appliations.
                    We are working on enabling macOS and Linux distros access to desktop applications.
                </p>
                <hr/>

                <div>
                    <h4>Register</h4>
                </div>
                <p>
                    Before you even start thinking about experiencing Federated Learning, please create new account.
                    <br> In order to do so, click <strong>"Register"</strong> at the right corner of blue navbar.
                    <br> Then you will be given 6 inputs to fill.
                    <br> Fill them with the appropiate values (e.g not common password, password no less than 8 characters).
                    <br> If any issue will occur it is going to come up at the top of the page.
                </p>
                <hr/>

                <div>
                    <h4>Log in</h4>
                </div>
                <p>
                After registration or if you haven't done it already please login using previously created credentials.

                </p>
                <hr/>

                <div>
                    <h4>Create first session</h4>
                </div>
                <p>
                    In order to create our first session click on the <strong>"Create new session"</strong> button
                </p>
                <hr/>

                <div>
                    <h4>Sessions panel</h4>
                </div>
                <p>
                    On our <strong> Sessions </strong> panel user is presented with all sessions created by anyone in our system.
                    <br> As you might observe we have two different <strong>paying plans</strong>.
                    <br> The general difference is the fact that <strong> Premium </strong> plan comes on-server model aggregation
                    <br> and allows users to create <strong>Private</strong> sessions.
                    <br> That is why, depeneding on the plan you chose different filter panel you will get.
                    <br> For the both of plans you have the following filters:
                    <ul>
                        <li>
                            Filter by session name
                        </li>
                         <li>
                            Filter by session tag
                        </li>
                        <li>
                            Show <strong>Created sessions</strong> checkbox filter
                        </li>
                         <li>
                            Show <strong>Joined sessions</strong> checkbox filter
                            <br> <span class="text-muted"> Notice that when you create session you also automatically join session.</span>
                        </li>
                    </ul>
                     For <strong> Premium </strong> plan you can additionally filter by:
                    <ul>
                        <li>
                            <strong>Public sessions</strong> checkbox filter
                        </li>
                        <li>
                            <strong>Private sessions</strong> checkbox filter
                        </li>
                    </ul>

                     If you just created your new session for the first time click checkbox name <strong>"Created sessions"</strong>.
                    <br> Then the only session you will see will be the one that you previously created.
                    <br>Click on newly created session card, then click <strong>"Go to session"</strong> button.

                </p>
                <hr/>

                <div>
                    <h4>Session panel</h4>
                </div>
                <p>
                    After going into session you will see session panel that is only presented to participants of the given session.
                    As you can see you have 3 different tabs:
                    <br>
                    <br>
                </p>
                <ul>
                    <li>
                        <h5> Information </h5>
                        <p>
                            In this tab, any session participant can read informations provided by session founder during the creation process
                            For instance, what learning rate was set, what model did owner choose etc.
                            In other words, this tab gives its participants usernames, any participant can see other usernames.
                        </p>

                    </li>
                    <li>
                        <h5> Learning panel</h5>
                        <p>
                            In order to do local learning, you must download <strong>ELL</strong>(<strong>E</strong>xecute  <strong>L</strong>ocal  <strong>L</strong>earning) desktop application.
                            After that, you will be able to run downloaded Python script with selected train and test data.
                            </p>

                             <button class='btn btn-primary btn btn-success mb-3 mx-3' @click="downloadMate()"> Download ELL app</button>
                              <br>
                            <p>
                            Only the session owner can aggregate results locally or on-server - depending on the pricing plan he or she has. If the owner has free plan the only action that is allowed is local aggreagtion.
                            In order to do so, one has to download <strong>ELL</strong>(<strong>A</strong>ggregate  <strong>L</strong>ocal  <strong>L</strong>earning) desktop application.
                            After that, you can run downloaded Python aggregation script with locally trained weights that other users uploaded.
                        </p>


                        <button class='btn btn-primary btn btn-success mb-3 mx-3' @click="downloadMates()"> Download ALL app</button>
                    </li>

                    <li>
                        <h5> Results </h5>
                        <p>
                            Here, you download aggregated weights at the end of each learning. In order for round to end, session owner needs to aggregate local weights.
                            After that, you can observe the accuracy results each user got locally for this round as well as the accuracy for aggregated weights.
                        </p>
                    </li>
                </ul>

            </section>
        </div>

    </div>
</div>
</template>
<script>
import axios from "axios"

export default {
  data() {
    return {

    }
  },
  methods:{
      downloadMate()
      {
           axios({
                url: 'api/v1/download-ell/' ,
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                console.log(response)
                var fileURL = window.URL.createObjectURL(new Blob([response.data], {
                    type: 'application/zip'
                }));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download','mate.zip');
                document.body.appendChild(fileLink);

                fileLink.click();

            })

      },
      downloadMates()
      {
          axios({
                url: 'api/v1/download-all/' ,
                method: 'GET',
                responseType: 'blob',
            }).then((response) => {
                console.log(response)
                var fileURL = window.URL.createObjectURL(new Blob([response.data], {
                    type: 'application/zip'
                }));
                var fileLink = document.createElement('a');

                fileLink.href = fileURL;
                fileLink.setAttribute('download','mates.zip');
                document.body.appendChild(fileLink);

                fileLink.click();

            })
      }
  }
}
</script>

