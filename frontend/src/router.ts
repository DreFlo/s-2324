import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { 
    path: '/',
    name: 'home',
    component: () => import('./pages/HomePage.vue')
  },
  {
    path: '/rankings/:numRankings?',
    name: 'rankings',
    component: () => import('./components/RankingTable.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router