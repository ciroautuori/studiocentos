<template>
  <BaseLayout
    title="Dashboard"
    subtitle="Panoramica dell'applicazione"
  >
    <div class="space-y-6">
      <!-- Statistiche -->
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Progetti Totali"
          :value="stats.projects"
          :icon="FolderIcon"
          icon-bg-color="bg-blue-50"
          icon-color="text-blue-600"
          :trend="stats.projects_trend"
          :trend-icon="ArrowTrendingUpIcon"
        />

        <StatCard
          title="Eventi Attivi"
          :value="stats.events"
          :icon="CalendarIcon"
          icon-bg-color="bg-green-50"
          icon-color="text-green-600"
          :trend="stats.events_trend"
          :trend-icon="ArrowTrendingUpIcon"
        />

        <StatCard
          title="Utenti Registrati"
          :value="stats.users"
          :icon="UserGroupIcon"
          icon-bg-color="bg-purple-50"
          icon-color="text-purple-600"
          :trend="stats.users_trend"
          :trend-icon="ArrowTrendingUpIcon"
        />

        <StatCard
          title="Visite Oggi"
          :value="stats.visits"
          :icon="ChartBarIcon"
          icon-bg-color="bg-yellow-50"
          icon-color="text-yellow-600"
          :trend="stats.visits_trend"
          :trend-icon="ArrowTrendingUpIcon"
        />
      </div>

      <!-- Progetti Recenti -->
      <RecentProjects
        :projects="recentProjects"
        :columns="projectColumns"
      />

      <!-- Eventi in Arrivo -->
      <UpcomingEvents
        :events="upcomingEvents"
        :columns="eventColumns"
      />
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BaseLayout from '../components/layout/BaseLayout.vue'
import StatCard from '../components/section/dashboard/StatCard.vue'
import RecentProjects from '../components/section/dashboard/RecentProjects.vue'
import UpcomingEvents from '../components/section/dashboard/UpcomingEvents.vue'
import {
  FolderIcon,
  CalendarIcon,
  UserGroupIcon,
  ChartBarIcon,
  ArrowTrendingUpIcon
} from '@heroicons/vue/24/outline'
import ApiService from '../services/ApiService'

const stats = ref({
  projects: 0,
  events: 0,
  users: 0,
  visits: 0,
  projects_trend: '+12%',
  events_trend: '+5%',
  users_trend: '+8%',
  visits_trend: '+15%'
})

const recentProjects = ref([])
const upcomingEvents = ref([])

const projectColumns = [
  { key: 'name', label: 'Nome' },
  { key: 'status', label: 'Stato' },
  { key: 'created_at', label: 'Data Creazione' }
]

const eventColumns = [
  { key: 'title', label: 'Titolo' },
  { key: 'date', label: 'Data' },
  { key: 'location', label: 'Luogo' }
]

const fetchStats = async () => {
  try {
    const response = await ApiService.getStats()
    stats.value = response.data
  } catch (error) {
    console.error('Errore nel caricamento delle statistiche:', error)
  }
}

const fetchRecentProjects = async () => {
  try {
    const response = await ApiService.getProjects({ limit: 5 })
    recentProjects.value = response.data
  } catch (error) {
    console.error('Errore nel caricamento dei progetti recenti:', error)
  }
}

const fetchUpcomingEvents = async () => {
  try {
    const response = await ApiService.getEvents({ upcoming: true, limit: 5 })
    upcomingEvents.value = response.data
  } catch (error) {
    console.error('Errore nel caricamento degli eventi in arrivo:', error)
  }
}

onMounted(() => {
  fetchStats()
  fetchRecentProjects()
  fetchUpcomingEvents()
})
</script>
