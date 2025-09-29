<template>
  <div class="min-h-screen bg-[#0b2a63]/5">
    <NavBar />

    <!-- Hero Section -->
    <div class="relative bg-[#0b2a63] overflow-hidden">
      <!-- Background Image -->
      <div class="absolute inset-0">
        <img src="@/assets/img/hero.jpg" alt="Hero Background" class="w-full h-full object-cover opacity-20" />
      </div>
      <!-- Decorative elements -->
      <div class="absolute top-0 left-0 w-1/3 h-full bg-red-600/10 skew-x-12 transform origin-top-left"></div>
      <div class="absolute bottom-0 right-0 w-96 h-96 rounded-full bg-red-600/10 blur-3xl"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full bg-red-600/5 blur-3xl"></div>

      <div class="container mx-auto px-4 lg:px-8 relative">
        <div class="max-w-4xl mx-auto py-24">
          <div class="text-center">
            <h1 class="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
              I Nostri <span class="text-red-600">Progetti</span>
            </h1>
            <p class="text-xl text-gray-200 mb-8 leading-relaxed">
              Scopri tutti i nostri progetti e iniziative per la comunità
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Search and Filter Section -->
    <div class="container mx-auto px-4 lg:px-8 -mt-8 relative z-10">
      <div class="max-w-5xl mx-auto">
        <div class="bg-white rounded-xl shadow-xl p-6 md:p-8">
          <div class="grid md:grid-cols-2 gap-6">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Cerca progetti..."
                class="w-full pl-12 pr-4 py-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#0b2a63] focus:border-[#0b2a63] focus:outline-none transition-all duration-200 text-lg"
              />
              <div class="absolute left-4 top-1/2 transform -translate-y-1/2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-[#0b2a63]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>

            <div>
              <select
                v-model="statusFilter"
                class="w-full px-4 py-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-[#0b2a63] focus:border-[#0b2a63] focus:outline-none transition-all duration-200 text-lg appearance-none bg-white"
              >
                <option value="">Tutti gli stati</option>
                <option value="In corso">In corso</option>
                <option value="Completato">Completato</option>
                <option value="Pianificato">Pianificato</option>
              </select>
              <div class="absolute right-4 top-1/2 transform -translate-y-1/2 pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[#0b2a63]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 lg:px-8 py-12">
      <!-- Loading state -->
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#0b2a63]"></div>
        <p class="mt-4 text-lg text-[#0b2a63]">Caricamento progetti...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="text-center py-12 max-w-xl mx-auto">
        <div class="bg-red-50 border border-red-200 text-[#0b2a63] px-6 py-5 rounded-lg shadow">
          <div class="flex items-center mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="font-medium">{{ error }}</p>
          </div>
          <button
            @click="fetchProjects"
            class="inline-flex items-center px-4 py-2 bg-[#0b2a63] hover:bg-[#0b2a63]/90 text-white font-medium rounded-lg transition-colors duration-300"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Riprova
          </button>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else-if="filteredProjects.length === 0" class="text-center py-16">
        <div class="bg-white p-8 rounded-xl shadow-lg max-w-xl mx-auto">
          <div class="w-24 h-24 mx-auto bg-[#0b2a63]/5 rounded-full flex items-center justify-center mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-[#0b2a63]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-xl font-bold text-[#0b2a63] mb-2">Nessun progetto trovato</h3>
          <p class="text-gray-600 mb-6">
            {{ searchQuery || statusFilter ? 'Nessun progetto corrisponde ai criteri di ricerca.' : 'Non ci sono progetti disponibili al momento.' }}
          </p>
          <button
            v-if="searchQuery || statusFilter"
            @click="resetFilters"
            class="inline-flex items-center text-[#0b2a63] hover:text-[#0b2a63]/80 font-medium transition-colors duration-300"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Azzera filtri
          </button>
        </div>
      </div>

      <!-- Projects grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="project in filteredProjects"
          :key="project.id"
          class="bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
        >
          <div class="relative h-64">
            <img
              v-if="project.thumbnail_url"
              :src="getImageUrl(project.thumbnail_url)"
              :alt="project.name"
              class="w-full h-full object-cover transition-transform duration-700 hover:scale-105"
            >
            <div v-else class="w-full h-full bg-gradient-to-br from-[#0b2a63]/5 to-[#0b2a63]/10 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-[#0b2a63]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="absolute top-4 right-4">
              <span class="text-xs font-medium bg-[#0b2a63]/10 text-[#0b2a63] py-1 px-3 rounded-full">
                {{ project.status || 'In corso' }}
              </span>
            </div>
            <div class="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-[#0b2a63]/80 to-transparent"></div>
          </div>

          <div class="p-6">
            <h3 class="text-xl font-bold text-[#0b2a63] mb-3 group-hover:text-[#0b2a63]/80 transition-colors duration-300">{{ project.name }}</h3>
            <p class="text-gray-600 mb-4 line-clamp-3">{{ project.description }}</p>

            <div class="flex items-center text-sm text-gray-500 mb-4" v-if="project.created_at">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ formatDate(project.created_at) }}
            </div>

            <router-link
              :to="{ name: 'ProjectDetail', params: { id: project.id }}"
              class="inline-flex items-center text-[#0b2a63] hover:text-[#0b2a63]/80 font-medium transition-colors duration-300"
            >
              Scopri di più
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </router-link>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="!loading && !error && filteredProjects.length > 0" class="mt-12 flex justify-center">
        <button
          class="mx-1 px-4 py-2 rounded-lg text-gray-700 hover:bg-[#0b2a63]/5 transition-colors duration-200"
          :class="{ 'bg-[#0b2a63] text-white': currentPage === 1 }"
          @click="currentPage = 1"
        >
          1
        </button>
        <button
          v-if="totalPages > 1"
          class="mx-1 px-4 py-2 rounded-lg text-gray-700 hover:bg-[#0b2a63]/5 transition-colors duration-200"
          :class="{ 'bg-[#0b2a63] text-white': currentPage === 2 }"
          @click="currentPage = 2"
        >
          2
        </button>
        <button
          v-if="totalPages > 2"
          class="mx-1 px-4 py-2 rounded-lg text-gray-700 hover:bg-[#0b2a63]/5 transition-colors duration-200"
          :class="{ 'bg-[#0b2a63] text-white': currentPage === 3 }"
          @click="currentPage = 3"
        >
          3
        </button>
      </div>
    </div>

    <SiteFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import ApiService from '@/services/ApiService';
import NavBar from '@/components/layout/NavBar.vue';
import SiteFooter from '@/components/layout/SiteFooter.vue';

const projects = ref([]);
const loading = ref(true);
const error = ref(null);
const API_BASE_URL = ApiService.baseURL();
const searchQuery = ref('');
const statusFilter = ref('');
const currentPage = ref(1);
const itemsPerPage = 9;

// Funzione per formattare le date
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('it-IT', options);
};

// Filtraggio progetti basato su ricerca e stato
const filteredProjects = computed(() => {
  let filtered = projects.value;

  // Filtra per stato
  if (statusFilter.value) {
    filtered = filtered.filter(project => {
      if (statusFilter.value === 'In corso') {
        return project.status === 'In corso';
      } else if (statusFilter.value === 'Completato') {
        return project.status === 'Completato';
      } else if (statusFilter.value === 'Pianificato') {
        return project.status === 'Pianificato';
      }
      return true;
    });
  }

  // Filtra per ricerca
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase().trim();
    filtered = filtered.filter(project => {
      return (
        project.name?.toLowerCase().includes(query) ||
        project.description?.toLowerCase().includes(query) ||
        project.category?.toLowerCase().includes(query)
      );
    });
  }

  return filtered;
});

const totalPages = computed(() => {
  return Math.ceil(filteredProjects.value.length / itemsPerPage);
});

// Funzione per resettare i filtri
const resetFilters = () => {
  searchQuery.value = '';
  statusFilter.value = '';
  currentPage.value = 1;
};

const getImageUrl = (thumbnailUrl) => {
  if (!thumbnailUrl) return null;
  if (thumbnailUrl.startsWith('http://') || thumbnailUrl.startsWith('https://')) {
    return thumbnailUrl;
  }
  return `${API_BASE_URL}${thumbnailUrl}`;
};

const fetchProjects = async () => {
  loading.value = true;
  error.value = null;

  try {
    const response = await ApiService.getProjects();
    projects.value = response.data;
  } catch (err) {
    error.value = 'Errore nel caricamento dei progetti. Riprova più tardi.';
    console.error('Error fetching projects:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchProjects();
});
</script>

<style scoped>
/* Stili specifici per garantire la coerenza dei colori */
.text-[#0b2a63] {
  color: #0b2a63;
}
.bg-[#0b2a63] {
  background-color: #0b2a63;
}
.bg-[#0b2a63]\/5 {
  background-color: rgba(11, 42, 99, 0.05);
}
.bg-[#0b2a63]\/10 {
  background-color: rgba(11, 42, 99, 0.1);
}
.bg-[#0b2a63]\/80 {
  background-color: rgba(11, 42, 99, 0.8);
}
.bg-[#0b2a63]\/90 {
  background-color: rgba(11, 42, 99, 0.9);
}
.hover\:bg-[#0b2a63]\/5:hover {
  background-color: rgba(11, 42, 99, 0.05);
}
.hover\:text-[#0b2a63]\/80:hover {
  color: rgba(11, 42, 99, 0.8);
}
.focus\:ring-[#0b2a63]:focus {
  --tw-ring-color: rgba(11, 42, 99, 0.5);
}
.focus\:border-[#0b2a63]:focus {
  border-color: #0b2a63;
}

/* Effetto hover sulle card */
.line-clamp-3 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}
</style>
