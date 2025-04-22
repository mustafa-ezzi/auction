import { setupLayouts } from 'virtual:generated-layouts'
import { createRouter, createWebHistory } from 'vue-router'
import routes from '~pages'
import PlayerRegistration from '../pages/register.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...setupLayouts(routes),
    {
      path: '/player-registration/:projectId',
      name: 'PlayerRegistration',
      component: PlayerRegistration,
    }
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to, from) => {
  const role = localStorage.getItem('role')

  if (to.name == 'all') {
    return true
  }else if(to.name == 'PlayerRegistration'){
    return true
  } else if (to.name == 'login') {
    if (role == 'team') {
      return { name: 'team-stats' }
    } else {
      return true
    }
  } else if (to.name == 'team-stats') {
    if (role == 'team') {
      return true
    } else {
      return { name: 'login' }
    }
  } else if (to.name == 'login') {
    if (role == 'superadmin') {
      return { name: 'settings' }
    } else {
      return true
    }
  } else {
    if (role == 'superadmin') {
      return true
    } else {
      return { name: 'login' }
    }
  }
})
export default router
