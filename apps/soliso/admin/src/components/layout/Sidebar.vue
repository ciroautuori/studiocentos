<template>
  <div class="flex flex-col h-full bg-gray-800 text-white">
    <div class="flex items-center justify-center h-16 px-4 border-b border-gray-700">
      <h1 class="text-xl font-bold">Soliso Admin</h1>
    </div>
    <nav class="flex-1 px-2 py-4 space-y-1">
      <router-link
        v-for="item in navigation"
        :key="item.name"
        :to="item.to"
        class="group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors"
        :class="[
          $route.path === item.to
            ? 'bg-gray-900 text-white'
            : 'text-gray-300 hover:bg-gray-700 hover:text-white'
        ]"
      >
        <component
          :is="item.icon"
          class="mr-3 h-5 w-5 transition-colors"
          :class="[
            $route.path === item.to
              ? 'text-white'
              : 'text-gray-400 group-hover:text-gray-300'
          ]"
        />
        {{ item.name }}
      </router-link>
    </nav>
    <div class="px-4 py-4 border-t border-gray-700">
      <div class="flex items-center mb-4">
        <img
          class="h-8 w-8 rounded-full"
          src="https://ui-avatars.com/api/?name=Admin"
          alt=""
        />
        <div class="ml-3">
          <p class="text-sm font-medium text-white">Admin</p>
          <p class="text-xs font-medium text-gray-400">Amministratore</p>
        </div>
      </div>
      <button
        @click="handleLogout"
        class="w-full flex items-center px-2 py-2 text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 rounded-md transition-colors"
      >
        <ArrowRightOnRectangleIcon class="mr-3 h-5 w-5" />
        Logout
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  HomeIcon,
  FolderIcon,
  CalendarIcon,
  UserGroupIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/vue/24/outline'
import AuthService from '@/services/AuthService'

export default {
  name: 'AppSidebar',
  components: {
    HomeIcon,
    FolderIcon,
    CalendarIcon,
    UserGroupIcon,
    Cog6ToothIcon,
    ArrowRightOnRectangleIcon
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const navigation = ref([
      { name: 'Dashboard', to: '/', icon: 'HomeIcon' },
      { name: 'Progetti', to: '/projects', icon: 'FolderIcon' },
      { name: 'Eventi', to: '/events', icon: 'CalendarIcon' },
      { name: 'Utenti', to: '/users', icon: 'UserGroupIcon' },
      { name: 'Impostazioni', to: '/settings', icon: 'Cog6ToothIcon' }
    ])

    const handleLogout = () => {
      AuthService.logout()
      router.push('/login')
    }

    return {
      navigation,
      handleLogout
    }
  }
}
</script>
