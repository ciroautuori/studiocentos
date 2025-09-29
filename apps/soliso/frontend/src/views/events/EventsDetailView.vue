<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />

    <div class="container mx-auto px-4 py-12">
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        <p class="mt-4 text-lg">Caricamento evento...</p>
      </div>

      <div v-else-if="error" class="text-center py-12">
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <p>{{ error }}</p>
          <router-link to="/events" class="mt-4 inline-block bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded">
            Torna agli eventi
          </router-link>
        </div>
      </div>

      <div v-else>
        <div class="mb-6 flex items-center">
          <router-link to="/events" class="flex items-center text-blue-600 hover:text-blue-800">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Torna alla lista eventi
          </router-link>
        </div>

        <div class="bg-white rounded-lg shadow-xl overflow-hidden">
          <!-- Banner con immagine e titolo -->
          <div class="relative h-64 md:h-80 w-full bg-blue-800">
            <img
              v-if="event.image_url"
              :src="getImageUrl(event.image_url)"
              :alt="event.title"
              class="w-full h-full object-cover"
            >
            <div v-else class="w-full h-full bg-gradient-to-r from-blue-700 to-purple-600"></div>

            <div class="absolute inset-0 flex flex-col justify-end p-8">
              <div v-if="event.is_featured" class="mb-4">
                <span class="bg-yellow-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                  In evidenza
                </span>
              </div>
              <h1 class="text-3xl md:text-4xl font-bold text-white drop-shadow-lg">{{ event.title }}</h1>
            </div>
          </div>

          <!-- Contenuto dell'evento -->
          <div class="p-6 md:p-8">
            <div class="flex flex-wrap gap-6 md:gap-12 mb-8">
              <!-- Data e ora -->
              <div class="flex items-start">
                <div class="text-blue-600 mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-gray-800">Data e ora</h3>
                  <p class="text-gray-600">
                    {{ formatDate(event.start_date) }}
                    <span v-if="event.start_date && formatTime(event.start_date)">
                      alle {{ formatTime(event.start_date) }}
                    </span>
                  </p>
                  <p v-if="event.end_date" class="text-gray-600">
                    <span class="font-medium">Fine:</span> {{ formatDate(event.end_date) }}
                    <span v-if="formatTime(event.end_date)">
                      alle {{ formatTime(event.end_date) }}
                    </span>
                  </p>
                </div>
              </div>

              <!-- Luogo -->
              <div v-if="event.location" class="flex items-start">
                <div class="text-blue-600 mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-gray-800">Luogo</h3>
                  <p class="text-gray-600">{{ event.location }}</p>
                </div>
              </div>

              <!-- Data creazione -->
              <div class="flex items-start">
                <div class="text-blue-600 mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 class="font-semibold text-gray-800">Pubblicato il</h3>
                  <p class="text-gray-600">{{ formatDate(event.created_at) }}</p>
                </div>
              </div>
            </div>

            <!-- Descrizione -->
            <div v-if="event.description" class="mb-8">
              <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Descrizione
              </h2>
              <div class="prose max-w-none">
                <p>{{ event.description }}</p>
              </div>
            </div>

            <!-- Immagini aggiuntive -->
            <div v-if="event.additional_images && event.additional_images.length > 0" class="mb-8">
              <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                Immagini dell'evento
              </h2>

              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                <div
                  v-for="(imgUrl, index) in event.additional_images"
                  :key="index"
                  class="relative aspect-video rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow"
                >
                  <img
                    :src="getImageUrl(imgUrl)"
                    :alt="`Immagine ${index + 1} dell'evento ${event.title}`"
                    class="w-full h-full object-cover"
                  />
                </div>
              </div>
            </div>

            <!-- Pulsanti di azione -->
            <div class="mt-10 flex flex-wrap gap-4">
              <router-link to="/events" class="inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Lista eventi
              </router-link>

              <button
                v-if="isAdmin"
                @click="navigateToEdit"
                class="inline-flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Modifica evento
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <SiteFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import ApiService from '@/services/ApiService';
import NavBar from '@/components/layout/NavBar.vue';
import SiteFooter from '@/components/layout/SiteFooter.vue';

const route = useRoute();
const event = ref({});
const loading = ref(true);
const error = ref(null);
const API_BASE_URL = ApiService.baseURL();

const getImageUrl = (thumbnailUrl) => {
  if (!thumbnailUrl) return null;
  if (thumbnailUrl.startsWith('http://') || thumbnailUrl.startsWith('https://')) {
    return thumbnailUrl;
  }
  return `${API_BASE_URL}${thumbnailUrl}`;
};

const fetchEvent = async () => {
  const eventId = route.params.id;
  loading.value = true;
  error.value = null;

  try {
    const response = await ApiService.getEvent(eventId);
    event.value = response.data;
  } catch (err) {
    error.value = 'Impossibile caricare i dettagli del progetto. Il progetto potrebbe non esistere o si è verificato un errore.';
    console.error('Error fetching event details:', err);
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';

  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  };

  try {
    return new Date(dateString).toLocaleDateString('it-IT', options);
  } catch (error) {
    console.error('Error formatting date:', error);
    return dateString;
  }
};

const formatTime = (dateString) => {
  if (!dateString) return '';

  try {
    const date = new Date(dateString);
    return date.toLocaleTimeString('it-IT', {
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (error) {
    console.error('Error formatting time:', error);
    return '';
  }
};

onMounted(() => {
  fetchEvent();
});
</script>
