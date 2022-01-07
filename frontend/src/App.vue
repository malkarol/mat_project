<template>
  <div class="d-flex flex-column h-100 Site">
    <NavBar />
     <div class="is-loading-bar has-text-centered" v-bind:class="{'is-loading': $store.state.isLoading }">
            <div class="lds-dual-ring"></div>
    </div>
    <div class="flex-shrink-0 Site-content">
        <router-view />
    </div>
    <Footer class="footer mt-auto py-3 bg-light"/>
  </div>

</template>

<script>
import axios from 'axios'
import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'
export default {
  name: 'App',
  components: {
    NavBar,
    Footer
  },
  beforeCreate () {
    this.$store.commit('initializeStore')

    if (this.$store.state.token) {
      axios.defaults.headers.common['Authorization'] = 'Token ' + this.$store.state.token
    } else {
      axios.defaults.headers.common['Authorization'] = ''
    }
  }

}
</script>
<style>
body{ height:100vh; margin:0; }
footer{ background:PapayaWhip; }

.Site {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

.Site-content {
  flex: 1;
}

/* Trick */
body{
  display:flex;
  flex-direction:column;
}

footer{
  margin-top:auto;
}

.lds-dual-ring {
    display: inline-block;
    width: 80px;
    height: 80px;
}

.lds-dual-ring:after {
    content: " ";
    display: block;
    width: 64px;
    height: 64px;
    margin: 8px;
    border-radius: 50%;
    border: 6px solid #ccc;
    border-color: #ccc transparent #ccc transparent;
    animation: lds-dual-ring 1.2s linear infinite;
}

@keyframes lds-dual-ring {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}

.is-loading-bar {
    height: 0;
    overflow: hidden;
    -webkit-transition: all 0.3s;
    transition: all 0.3s;


}

.is-loading-bar.is-loading {
        height: 80px;
    }
</style>
