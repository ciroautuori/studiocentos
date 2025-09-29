<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Mobile menu button -->
    <div class="lg:hidden">
      <button
        @click="isSidebarOpen = !isSidebarOpen"
        class="fixed top-4 left-4 z-50 p-2 rounded-md text-gray-500 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
      >
        <span class="sr-only">Apri menu</span>
        <Bars3Icon v-if="!isSidebarOpen" class="h-6 w-6" />
        <XMarkIcon v-else class="h-6 w-6" />
      </button>
    </div>

    <!-- Sidebar -->
    <div
      class="fixed inset-y-0 left-0 z-40 w-64 transform transition-transform duration-200 ease-in-out lg:translate-x-0"
      :class="{
        'translate-x-0': isSidebarOpen,
        '-translate-x-full': !isSidebarOpen
      }"
    >
      <AppSidebar />
    </div>

    <!-- Main content -->
    <div class="lg:pl-64 flex flex-col min-h-screen">
      <AppNavbar />

      <main class="flex-1">
        <div class="py-6">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="mb-6">
              <h1 class="text-2xl font-semibold text-gray-900">{{ title }}</h1>
              <p class="mt-1 text-sm text-gray-500">{{ subtitle }}</p>
            </div>
            <slot></slot>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import AppNavbar from './Navbar.vue'
import AppSidebar from './Sidebar.vue'
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'BaseLayout',
  components: {
    AppNavbar,
    AppSidebar,
    Bars3Icon,
    XMarkIcon
  },
  props: {
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      default: ''
    }
  },
  setup() {
    const isSidebarOpen = ref(false)

    return {
      isSidebarOpen
    }
  }
}
</script>
