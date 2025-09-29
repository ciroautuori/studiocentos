import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
  },
  {
    path: '/projects',
    name: 'projects-list',
    component: () => import('../views/projects/ProjectsListView.vue'),
  },
  {
    path: '/projects/:id',
    name: 'ProjectDetail',
    component: () => import('../views/projects/ProjectsDetailView.vue'),
  },
  {
    path: '/events',
    name: 'events-list',
    component: () => import('@/views/events/EventsListView.vue'),
    props: true
  },
  {
    path: '/events/:id',
    name: 'events-detail',
    component: () => import('@/views/events/EventsDetailView.vue'),
    props: true
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
