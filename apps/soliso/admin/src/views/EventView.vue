<template>
  <div class="bg-white rounded-lg shadow">
    <div class="border-b border-gray-200 bg-gray-50 px-4 py-5 sm:px-6">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <h3 class="text-lg font-medium leading-6 text-gray-900">Event Details</h3>
        <div class="mt-4 flex flex-col sm:mt-0 sm:flex-row sm:space-x-3 space-y-3 sm:space-y-0">
          <router-link v-if="event" :to="{ name: 'event-edit', params: { id: event.id } }"
            class="inline-flex items-center justify-center rounded-md border border-transparent bg-yellow-500 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 transition-colors duration-150">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit Event
          </router-link>
          <router-link :to="{ name: 'events-list' }"
            class="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-150">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Events
          </router-link>
        </div>
      </div>
    </div>

    <div class="p-6">
      <div v-if="loading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
        <p class="mt-2 text-gray-600">Loading event details...</p>
      </div>
      <div v-if="error" class="rounded-md bg-red-50 p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">{{ error }}</h3>
          </div>
        </div>
      </div>

      <div v-if="!loading && event" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-6">
            <div class="bg-white shadow rounded-lg overflow-hidden">
              <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 class="text-lg font-medium leading-6 text-gray-900">Basic Information</h3>
              </div>
              <div class="px-4 py-5 sm:p-6">
                <dl class="space-y-4">
                  <div>
                    <dt class="text-sm font-medium text-gray-500">Title</dt>
                    <dd class="mt-1 text-gray-900">{{ event.title }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500">Description</dt>
                    <dd class="mt-1 text-gray-900 whitespace-pre-line">{{ event.description || 'No description provided' }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500">Active</dt>
                    <dd class="mt-1">
                      <ActiveBadge :is-active="event.is_featured" />
                    </dd>
                  </div>
                </dl>
              </div>
            </div>

            <div class="bg-white shadow rounded-lg overflow-hidden">
              <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 class="text-lg font-medium leading-6 text-gray-900">Timestamps</h3>
              </div>
              <div class="px-4 py-5 sm:p-6">
                <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <dt class="text-sm font-medium text-gray-500">Created At</dt>
                    <dd class="mt-1 text-gray-900">{{ formatDate(event.created_at) }}</dd>
                  </div>
                  <div>
                    <dt class="text-sm font-medium text-gray-500">Updated At</dt>
                    <dd class="mt-1 text-gray-900">{{ formatDate(event.updated_at) }}</dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>

          <div class="bg-white shadow rounded-lg overflow-hidden">
            <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 class="text-lg font-medium leading-6 text-gray-900">Event Image</h3>
            </div>
            <div class="px-4 py-5 sm:p-6">
              <EventImage :image-url="event.image_url" :alt-text="event.title" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import ApiService from '../services/ApiService';
import { formatDate } from '../utils/dateUtils';
import EventImage from '../components/ui/images/EventImage.vue';
import ActiveBadge from '../components/ui/badges/ActiveBadge.vue';

const route = useRoute();
const event = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchEvent = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await ApiService.getEvent(route.params.id);
    event.value = response.data;
  } catch (err) {
    console.error("Failed to fetch event:", err);
    error.value = 'Failed to load event details. Please try again later.';
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = `Error: ${err.response.data.detail}`;
    }
  } finally {
    loading.value = false;
  }
};

onMounted(fetchEvent);
</script>
