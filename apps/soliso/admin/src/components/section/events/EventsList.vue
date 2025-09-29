<template>
  <BaseLayout
    title="Gestione Eventi"
    subtitle="Visualizza e gestisci gli eventi"
  >
    <div class="bg-white p-3 sm:p-4 md:p-6 rounded-lg shadow">
      <PageHeader title="Events">
        <template #actions>
          <router-link :to="{ name: 'event-create' }"
            class="w-full sm:w-auto bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition duration-300 text-center flex items-center justify-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Event
          </router-link>
        </template>
      </PageHeader>

      <div v-if="loading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
        <p class="mt-2 text-gray-600">Loading events...</p>
      </div>
      <div v-if="error" class="text-red-500 bg-red-100 p-3 sm:p-4 rounded-lg mb-4">{{ error }}</div>

      <div v-if="!loading && events.length === 0" class="text-center py-8 text-gray-500">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="mt-2">No events found. Add one!</p>
      </div>

      <div v-if="!loading && events.length > 0" class="overflow-x-auto -mx-3 sm:mx-0">
        <div class="min-w-full inline-block align-middle">
          <div class="overflow-hidden border border-gray-200 rounded-lg">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th scope="col" class="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                  <th scope="col" class="px-3 sm:px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Image</th>
                  <th scope="col" class="hidden sm:table-cell px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Active</th>
                  <th scope="col" class="px-3 sm:px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="event in events" :key="event.id" class="hover:bg-gray-50 transition-colors duration-150">
                  <td class="px-3 sm:px-4 py-3 whitespace-nowrap text-sm text-gray-900">{{ event.id }}</td>
                  <td class="px-3 sm:px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">{{ event.title }}</td>
                  <td class="px-3 sm:px-4 py-3 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="h-10 w-10 sm:h-12 sm:w-12 flex-shrink-0">
                        <EventImage :image-url="event.image_url" :alt-text="event.title" size="150x150" />
                      </div>
                    </div>
                  </td>
                  <td class="hidden sm:table-cell px-4 py-3 whitespace-nowrap">
                    <ActiveBadge :is-active="event.is_featured" />
                  </td>
                  <td class="px-3 sm:px-4 py-3 whitespace-nowrap text-center text-sm font-medium">
                    <div class="flex justify-center space-x-2">
                      <router-link :to="{ name: 'event-view', params: { id: event.id } }"
                        class="text-blue-500 hover:text-blue-700 transition-colors duration-150 p-1 rounded-full hover:bg-blue-50" title="View">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                      </router-link>
                      <router-link :to="{ name: 'event-edit', params: { id: event.id } }"
                        class="text-yellow-500 hover:text-yellow-700 transition-colors duration-150 p-1 rounded-full hover:bg-yellow-50" title="Edit">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </router-link>
                      <button @click="confirmDelete(event.id)" class="text-red-500 hover:text-red-700 transition-colors duration-150 p-1 rounded-full hover:bg-red-50" title="Delete">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ApiService from '../../../services/ApiService';
import PageHeader from '../../../components/ui/headers/PageHeader.vue';
import EventImage from '../../../components/ui/images/EventImage.vue';
import ActiveBadge from '../../../components/ui/badges/ActiveBadge.vue';
import BaseLayout from '../../../components/layout/BaseLayout.vue';

const events = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchEvents = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await ApiService.getEvents();
    events.value = response.data;
  } catch (err) {
    console.error("Failed to fetch events:", err);
    error.value = 'Failed to load events. Please try again later.';
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = `Error: ${err.response.data.detail}`;
    }
  } finally {
    loading.value = false;
  }
};

const confirmDelete = (id) => {
  if (window.confirm(`Are you sure you want to delete event ${id}? This action cannot be undone.`)) {
    deleteEvent(id);
  }
};

const deleteEvent = async (id) => {
  try {
    await ApiService.deleteEvent(id);
    events.value = events.value.filter(p => p.id !== id);
    alert(`Event ${id} deleted successfully.`);
  } catch (err) {
    console.error(`Failed to delete event ${id}:`, err);
    error.value = `Failed to delete event ${id}.`;
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = `Error deleting: ${err.response.data.detail}`;
    }
    alert(error.value);
  }
};

onMounted(fetchEvents);
</script>
