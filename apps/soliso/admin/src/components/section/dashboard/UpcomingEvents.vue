<template>
  <div class="bg-white shadow rounded-lg transition-all duration-300 hover:shadow-lg">
    <div class="px-4 py-5 sm:px-6">
      <div class="flex items-center justify-between">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Eventi in Arrivo
        </h3>
        <router-link
          to="/events"
          class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
        >
          Vedi tutti
        </router-link>
      </div>
    </div>
    <div class="border-t border-gray-200">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th v-for="column in columns" :key="column.key"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ column.label }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="event in events" :key="event.id"
              class="hover:bg-gray-50 transition-colors duration-150">
              <td v-for="column in columns" :key="column.key"
                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <template v-if="column.key === 'date'">
                  {{ formatDate(event[column.key]) }}
                </template>
                <template v-else>
                  {{ event[column.key] }}
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatDate } from '../../../utils/dateUtils'

const props = defineProps({
  events: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  }
})
</script>
