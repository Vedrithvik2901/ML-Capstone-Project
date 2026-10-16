import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import DatasetExplorer from '../pages/DatasetExplorer.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/datasets',
      name: 'datasets',
      component: DatasetExplorer,
    },
  ],
})

export default router
