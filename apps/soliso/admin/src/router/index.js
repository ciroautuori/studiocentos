// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import AuthService from '@/services/AuthService'

// Importa le viste per i progetti
import ProjectsList from '../components/section/projects/ProjectsList.vue'
import ProjectEdit from '../components/section/projects/ProjectEdit.vue'
import ProjectCreate from '../components/section/projects/ProjectCreate.vue'

// Importa le viste per gli eventi
import EventsList from '../components/section/events/EventsList.vue'
import EventEdit from '../components/section/events/EventEdit.vue'
import EventCreate from '../components/section/events/EventCreate.vue'

// Importa le viste principali
import Dashboard from '../views/DashboardView.vue'
import ProjectView from '../views/ProjectView.vue'
import EventView from '@/views/EventView.vue'
import LoginView from '@/views/LoginView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'home',
    component: Dashboard,
    meta: { requiresAuth: true }
  },

  // Rotte per i progetti
  {
    path: '/projects',
    name: 'projects-list',
    component: ProjectsList,
    meta: { requiresAuth: true }
  },
  {
    path: '/projects/new',
    name: 'project-create',
    component: ProjectCreate,
    meta: { requiresAuth: true }
  },
  {
    path: '/projects/:id',
    name: 'project-view',
    component: ProjectView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/projects/:id/edit',
    name: 'project-edit',
    component: ProjectEdit,
    props: true,
    meta: { requiresAuth: true }
  },

  // Rotte per gli eventi
  {
    path: '/events',
    name: 'events-list',
    component: EventsList,
    meta: { requiresAuth: true }
  },
  {
    path: '/events/new',
    name: 'event-create',
    component: EventCreate,
    meta: { requiresAuth: true }
  },
  {
    path: '/events/:id',
    name: 'event-view',
    component: EventView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/events/:id/edit',
    name: 'event-edit',
    component: EventEdit,
    props: true,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = AuthService.isAuthenticated()

  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
