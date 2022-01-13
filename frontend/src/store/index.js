import { createStore } from 'vuex'

export default createStore({
  state: {
    isLoading: false,
    isAuthenticated: false,
    token: '',
    user: {
      id: 0,
      username: '',
      pricing_plan: 1
    }
  },
  mutations: {
    initializeStore (state) {
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
        state.user.username = localStorage.getItem('username')
        state.user.id = localStorage.getItem('userid')
        state.user.pricing_plan = localStorage.getItem('pricing_plan')

      } else {
        state.token = ''
        state.isAuthenticated = false
        state.user.username = ''
        state.user.id = ''
        state.user.pricing_plan = 1
      }
    },
    setIsLoading (state, status) {
      state.isLoading = status
    },
    setToken (state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    removeToken (state) {
      state.token = ''
      state.isAuthenticated = false
    },
    setUser(state, user){
      state.user = user
    }
  },
  actions: {

  },
  modules: {

  }
})
