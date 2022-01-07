<template>
<div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
    <div class="card border-0 shadow rounded-3 my-5">
        <div class="card-body p-4 p-sm-5 mb-5">
            <div>
                <h3>Your Profile</h3>
                <hr />
            </div>
            <nav>
                <div class="nav nav-tabs mb-4" id="nav-tab" role="tablist">
                    <button class="nav-link active" id="nav-home-tab" data-bs-toggle="tab" data-bs-target="#nav-general" type="button" role="tab" aria-controls="nav-home" aria-selected="true">General information</button>
                    <button class="nav-link" id="nav-password-tab" data-bs-toggle="tab" data-bs-target="#nav-password" type="button" role="tab" aria-controls="nav-password" aria-selected="false">Change password</button>
                    <button class="nav-link" id="nav-email-tab" data-bs-toggle="tab" data-bs-target="#nav-email" type="button" role="tab" aria-controls="nav-email" aria-selected="false">Change e-mail</button>
                </div>
            </nav>
            <div class="tab-content" id="nav-tabContent">
                <div class="tab-pane fade show active" id="nav-general" role="tabpanel" aria-labelledby="nav-home-tab">
                    <form v-if="!isFetching" @submit.prevent="submitForm" class="row g-3 needs-validation" oninput='inputPasswordConfirm.setCustomValidity(inputPasswordConfirm.value != inputPassword.value ? "Passwords do not match." : "");
                        inputEmailConfirm.setCustomValidity(inputEmailConfirm.value != inputEmail.value ? "Passwords do not match." : "");' novalidate>
                        <div class="col-md-6 position-relative">
                            <label for="inputUserName" class="form-label">User name</label>
                            <input readonly type="text" class="form-control" id="inputUserName" v-model="username" required />
                        </div>
                        <div class="col-md-6 has-validation">
                            <label for="inputFullName" class="form-label">Full Name</label>
                            <input readonly type="text" class="form-control" id="inputFullName" v-model="fullName" required />
                        </div>
                        <div class="my-5 col-md-6">
                            <label for="mlInput" class="form-label">Machine Learning background</label>
                            <select disabled readonly id="mlInput" class="form-select" required v-model="mlBackground">
                                <option value="" selected disabled hidden>Choose...</option>
                                <option value="1">Student</option>
                                <option value="2">Professor</option>
                                <option value="3">Professional</option>
                                <option value="4">Hobbyst</option>
                            </select>
                        </div>
                        <div class="my-5 col-md-6">
                            <label for="planInput" class="form-label">Pricing Plan</label>
                            <select disabled id="planInput" class="form-select" required v-model="pricingPlan">
                                <option value="" selected disabled hidden>...</option>
                                <option value="1">Free</option>
                                <option value="2">Premium</option>
                            </select>
                        </div>
                        <div class="col-12 d-flex justify-content-between">
                            <input id="editButton" value="Edit your information" type="button" class="btn btn-primary" @click="switchEdit()" />
                            <input id="saveButton" value="Save changes" type="button" class="btn btn-success d-none" @click="changeInformation()" />
                        </div>
                    </form>
                </div>
                <div class="tab-pane fade show" id="nav-password" role="tabpanel" aria-labelledby="nav-password-tab">
                    <div id="passChangeInput" class="card-body border border-2 rounded-3 my-3 border-success">
                        <label class="text-success"><strong>Successfully changed password!</strong></label>
                    </div>
                    <form v-if="!isFetching" class="row g-3 needs-val" oninput='inputPasswordConfirm.setCustomValidity(inputPasswordConfirm.value != inputPassword.value ? "Passwords do not match." : "");
                        inputEmailConfirm.setCustomValidity(inputEmailConfirm.value != inputEmail.value ? "Passwords do not match." : "");' novalidate>
                        <div class="col-md-6">
                            <label for="inputPassword" class="form-label">Password</label>
                            <input type="password" class="readonly form-control" id="inputPassword" v-model="changedPassword" required />
                        </div>
                        <div class="col-md-6 ">
                            <label readonly for="inputPasswordConfirm" class="form-label">
                                Repeat password</label>
                            <input type="password" class="form-control" id="inputPasswordConfirm" required />
                            <div class="invalid-feedback">Passwords do not match</div>
                        </div>
                        <div class="col-md-12">
                            <small id="passwordHelpBlock" class="form-text text-muted">
                                Your password must be 8-20 characters long, contain letters and
                                numbers, and must not contain spaces, special characters, or
                                emoji.
                            </small>
                        </div>
                        <div class="col-12">
                            <input value="Change password" type="button" class="btn btn-success" @click="changePassword()" />
                        </div>
                    </form>
                </div>
                <div class="tab-pane fade show" id="nav-email" role="tabpanel" aria-labelledby="nav-email-tab">
                    <div id="emailChangeInput" class="card-body border border-2 rounded-3 my-3 border-success d-none">
                        <label class="text-success"><strong>Successfully changed e-mail!</strong></label>
                    </div>
                    <form class="row g-3 needs-val-email" @change='checkEmails()' novalidate>
                        <div class="col-md-6">
                            <label for="inputEmail" class="form-label">Email</label>
                            <input type="email" class="form-control" id="inputEmail" v-model="email" required />
                        </div>
                        <div class="col-md-6">
                            <label for="inputEmailConfirm" class="form-label">Repeat email</label>
                            <input type="email" class="form-control" id="inputEmailConfirm" required aria-describedby="validationServer03Feedback" />
                        </div>
                        <div id="emailFeedbackBad" class="invalid-feedback">
                            E-mails must be valid and be the same.
                        </div>
                        <div class="col-12 mt-5">
                            <input value="Change e-mail" type="button" class="btn btn-success" @click="changeEmail()" />
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            isModalVisible: false,
            isFetching: true,
            username: '',
            password: '',
            email: '',
            fullName: '',
            pricingPlan: '',
            changedPassword: '',
            mlBackground: '',
            errors: [],
            isEditing: false,
        }
    },
    mounted() {
        this.getUserData()

        passChangeInput.classList.add("d-none")
        emailChangeInput.classList.add("d-none")
    },
    methods: {
        sleep(miliseconds) {
            var currentTime = new Date().getTime();

            while (currentTime + miliseconds >= new Date().getTime()) {}
        },
        enableInputs() {
            inputUserName.readOnly = false
            inputFullName.readOnly = false
            planInput.disabled = false
            mlInput.disabled = false
        },
        disableInputs() {

        },

        checkEmails() {
            if (this.email == inputEmailConfirm.value) {
                emailFeedbackBad.classList.remove('d-flex')
            } else {
                emailFeedbackBad.classList.add('d-flex')
            }
            return this.email == inputEmailConfirm.value
        },
        changeEmail() {
            this.validateEmail()
            if (!this.checkEmails()) {
                return
            }

            const formData = {
                user_id: this.$store.state.user.id,
                email: this.email
            }
            console.log(formData)
            axios
                .post('profileEmail/', formData)
                .then(response => {
                    console.log(response)
                    emailChangeInput.classList.remove('d-none')
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else if (error.message) {
                        this.errors.push('Something went wrong. Please try again.')
                    }
                })
        },
        getUserData() {
            axios.get('user/' + this.$store.state.user.id)
                .then((resp) => {
                    console.log(resp.data)
                    this.username = resp.data.username
                    this.email = resp.data.email
                    this.fullName = resp.data.first_name + ' ' + resp.data.last_name
                    this.pricingPlan = resp.data.pricing_plan < 1 ? 1 : resp.data.pricing_plan
                    this.mlBackground = resp.data.ml_background
                    this.isFetching = false
                })
        },
        changeInformation() {
            this.validateForm()

            saveButton.classList.remove('d-flex')
            editButton.value = "Edit your information"
            this.isEditing = false

            const formData = {
                user_id: this.$store.state.user.id,
                username: this.username,
                fullname: this.fullName,
                pricingPlan: this.pricingPlan,
                mlBackground: this.mlBackground
            }

            axios
                .post('profileManagement/', formData)
                .then(response => {
                    
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else if (error.message) {
                        this.errors.push('Something went wrong. Please try again.')
                    }
                })

        },
        changePassword() {
            this.validatePassword()
            if (this.password != inputPasswordConfirm.value) {
                console.log("Hello")
                return
            }
            const formData = {
                user_id: this.$store.state.user.id,
                password: this.changedPassword
            }

            axios
                .post('profilePassword/', formData)
                .then(response => {
                    var element = document.getElementById("passChangeInput");
                    element.classList.remove("d-none")
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else if (error.message) {
                        this.errors.push('Something went wrong. Please try again.')
                    }
                })
        },
        canISeeModel() {
            return this.isModalVisible
        },
        toggleModalAlert() {
            console.log("hej")
            this.isModalVisible = false
        },
        switchEdit() {
            if (this.isEditing) {
                this.isFetching = true
                this.getUserData()
                editButton.value = "Edit your information"
                editButton.classList.remove('btn-danger')
                editButton.classList.add('btn-primary')
                saveButton.classList.add('d-none')
                this.isEditing = false
            } else {
                this.isEditing = true

                this.enableInputs()

                saveButton.classList.remove('d-none')
                editButton.classList.remove('btn-primary')
                editButton.classList.add('btn-danger')
                editButton.value = "Discard changes"
            }
        },
        validateForm() {
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

        validatePassword() {
            var forms = document.querySelectorAll('.needs-val')

            // Loop over them and prevent submission
            Array.prototype.slice.call(forms).forEach(function (form) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            })
        },

        validateEmail() {
            var forms = document.querySelectorAll('.needs-val-email')

            // Loop over them and prevent submission
            Array.prototype.slice.call(forms).forEach(function (form) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            })
        }
    }
}
</script>
