<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <NavBar />

    <div class="container mx-auto px-4 py-12">
      <!-- Loading state -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-20">
        <div class="relative w-24 h-24">
          <div class="absolute top-0 left-0 w-full h-full border-4 border-gray-200 rounded-full"></div>
          <div class="absolute top-0 left-0 w-full h-full border-4 border-t-blue-500 border-r-transparent border-b-transparent border-l-transparent rounded-full animate-spin"></div>
        </div>
        <p class="mt-6 text-xl font-medium text-gray-600">Caricamento progetto...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="max-w-xl mx-auto py-12 px-6">
        <div class="bg-red-50 border-l-4 border-red-500 rounded-lg overflow-hidden shadow-lg">
          <div class="p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-red-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-lg font-medium text-red-800">Si è verificato un errore</h3>
                <p class="mt-2 text-red-700">{{ error }}</p>
              </div>
            </div>
            <div class="mt-6 flex justify-center">
              <router-link to="/" class="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200">
                <svg class="mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Torna alla home
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Project details -->
      <div v-else class="max-w-5xl mx-auto transform transition-all duration-500 opacity-100 translate-y-0">
        <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
          <!-- Project header with image background -->
          <div class="relative h-80 bg-gray-900">
            <div class="absolute inset-0 overflow-hidden">
              <img
                v-if="project.thumbnail_url"
                :src="getImageUrl(project.thumbnail_url)"
                :alt="project.name"
                class="w-full h-full object-cover filter blur-sm opacity-40 transform scale-105"
              >
            </div>

            <div class="absolute inset-0 flex items-center justify-center">
              <div class="max-w-md px-6 text-center">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 mb-6">
                  {{ project.status || 'In corso' }}
                </span>
                <h1 class="text-4xl font-bold text-white leading-tight mb-2">{{ project.name }}</h1>
                <p class="text-gray-300 text-sm">
                  Creato il {{ formatDate(project.created_at) }}
                </p>
              </div>
            </div>
          </div>

          <div class="md:flex">
            <!-- Left column - Image -->
            <div class="md:w-1/2 p-6">
              <div class="rounded-xl overflow-hidden shadow-md bg-gray-50 aspect-video">
                <img
                  v-if="project.thumbnail_url"
                  :src="getImageUrl(project.thumbnail_url)"
                  :alt="project.name"
                  class="w-full h-full object-cover"
                >
                <div v-else class="w-full h-full flex items-center justify-center">
                  <svg class="w-20 h-20 text-gray-300" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>
            </div>

            <!-- Right column - Details -->
            <div class="md:w-1/2 p-6">
              <div class="space-y-8">
                <div>
                  <h2 class="text-xl font-semibold text-gray-900 mb-3">Descrizione</h2>
                  <div class="prose prose-blue max-w-none text-gray-600">
                    <p>{{ project.description }}</p>
                  </div>
                </div>

                <div v-if="project.website || project.location" class="space-y-6">
                  <div v-if="project.website" class="flex items-start">
                    <div class="flex-shrink-0">
                      <svg class="h-6 w-6 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                      </svg>
                    </div>
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-gray-500">Sito Web</h3>
                      <a :href="project.website" target="_blank" rel="noopener noreferrer"
                         class="text-blue-600 hover:text-blue-800 transition-colors duration-200">
                        {{ project.website }}
                      </a>
                    </div>
                  </div>

                  <div v-if="project.location" class="flex items-start">
                    <div class="flex-shrink-0">
                      <svg class="h-6 w-6 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    </div>
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-gray-500">Luogo</h3>
                      <p class="text-gray-900">{{ project.location }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-10 pt-6 border-t border-gray-200">
                <router-link to="/projects" class="inline-flex items-center px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors duration-200">
                  <svg class="mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16l-4-4m0 0l4-4m-4 4h18" />
                  </svg>
                  Torna alla lista progetti
                </router-link>
              </div>
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
const project = ref({});
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

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('it-IT', options);
};

const fetchProject = async () => {
  const projectId = route.params.id;
  loading.value = true;
  error.value = null;

  try {
    const response = await ApiService.getProject(projectId);
    project.value = response.data;
    // Aggiungiamo un breve delay per mostrare l'animazione di caricamento
    setTimeout(() => {
      loading.value = false;
    }, 300);
  } catch (err) {
    error.value = 'Impossibile caricare i dettagli del progetto. Il progetto potrebbe non esistere o si è verificato un errore.';
    console.error('Error fetching project details:', err);
    loading.value = false;
  }
};

onMounted(() => {
  fetchProject();
});
</script>

<style scoped>
/* Opzionale: aggiungere stili CSS specifici */
.prose p {
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}
</style>
