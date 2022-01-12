<template>
<div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
    <div v-if="errors.length" class="alert alert-danger d-flex align-items-center" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:">
            <use xlink:href="#exclamation-triangle-fill" /></svg>
        <div v-for="error in errors" v-bind:key="error">
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
                    <input v-model="checked" class="form-check-input" type="checkbox" value="" id="rememberPasswordCheck">
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
    data() {
        return {
            password: '',
            email: '',
            errors: [],
            checked: false
        }
    },
    mounted() {
        this.getCookie()
    },
    methods: {
        getCookie() {
            if (document.cookie.length > 0) {
                let arr = document.cookie.split(";"); // the format shown here needs to be cut to output its own
                const decipher = salt => {
                    const textToChars = text => text.split('').map(c => c.charCodeAt(0));
                    const applySaltToChar = code => textToChars(salt).reduce((a, b) => a ^ b, code);
                    return encoded => encoded.match(/.{1,2}/g)
                        .map(hex => parseInt(hex, 16))
                        .map(applySaltToChar)
                        .map(charCode => String.fromCharCode(charCode))
                        .join('');
                }

                const myDecipher = decipher('ThisIsAVerySafePassword')
                for (let i = 0; i < arr.length; i++) {
                    let arr2 = arr[i].split("="); // cut again
                    //Judge the corresponding value of search
                    if (arr2[0] == "email") {
                        this.email = arr2[1]; // save to the place where the data is saved
                    } else if (arr2[0] == " Pwd") {
                        this.password = myDecipher(arr2[1]);
                    }
                }
            }
        },
        setCookie() {
            let exdate = new Date()
            exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * 30); // number of days saved
            const Cipher = salt => {
                const textToChars = text => text.split('').map(c => c.charCodeAt(0));
                const byteHex = n => ("0" + Number(n).toString(16)).substr(-2);
                const applySaltToChar = code => textToChars(salt).reduce((a, b) => a ^ b, code);

                return text => text.split('')
                    .map(textToChars)
                    .map(applySaltToChar)
                    .map(byteHex)
                    .join('');
            }
            const cipher = Cipher('ThisIsAVerySafePassword')
            //String concatenation cookie
            window.document.cookie = "email" + "=" + this.email + ";path=/;expires=" + exdate.toGMTString();
            window.document.cookie = "Pwd" + "=" + cipher(this.password) + ";path=/;expires=" + exdate.toGMTString();
        },
        async submitForm() {
            this.$store.commit('setIsLoading', true)
            axios.defaults.headers.common['Authorization'] = ''
            localStorage.removeItem('token')

            if (this.checked) {
                this.setCookie()
            }

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
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else if (error.message) {
                        this.errors.push('Something went wrong. Please try again.')
                    }
                })

            await axios
                .get('/api/v1/users/me/')
                .then(response => {
                    console.log(response)
                    this.$store.commit('setUser', {
                        'id': response.data.id,
                        'username': response.data.username,
                        'pricing_plan': response.data.pricing_plan
                    })

                    localStorage.setItem('username', response.data.username)
                    localStorage.setItem('userid', response.data.id)
                    localStorage.setItem('pricing_plan', response.data.pricing_plan)

                    this.$router.push('/sessions')
                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsLoading', false)

        }
    }
}
</script>
