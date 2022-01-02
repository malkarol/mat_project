import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
const routes = [
  {
    path: '/login',
    name: 'Login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',

    component: () => import(/* webpackChunkName: "about" */ '../views/Register.vue')
  },
  {
    path: '/sessions',
    name: 'SessionsPanel',
    meta: {
      requireLogin: true
    },
    component: () => import(/* webpackChunkName: "about" */ '../views/SessionsPanel.vue')
  },
  {
    path: '/session',
    name: 'SingleSession',
    meta: {
      requireLogin: true
    },
    component: () => import(/* webpackChunkName: "about" */ '../views/SingleSession.vue')
  },
  {
    path: '/',
    name: 'Home',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Home.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
