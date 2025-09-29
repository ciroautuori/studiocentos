<template>
  <section id="projects" class="section relative overflow-hidden bg-gray-50 py-24">
    <!-- Elementi decorativi avanzati di sfondo -->
    <div class="absolute top-0 left-0 w-1/3 h-full bg-blue/5 skew-x-12 transform origin-top-left"></div>
    <div class="absolute -bottom-10 -right-10 w-72 h-72 rounded-full bg-red/5 animate-pulse-slow"></div>
    <div class="absolute top-1/4 right-1/4 w-16 h-16 rounded-full bg-red/10 animate-float"></div>
    <div class="absolute bottom-1/3 left-1/5 w-12 h-12 rounded-full bg-blue/10 animate-float-delayed"></div>

    <div class="container-custom relative z-10">
      <SectionHeader
        title="Progetti"
        subtitle="Scopri i progetti e le iniziative che stiamo portando avanti per fare la differenza nella nostra comunità."
        label="Progetti"
        titlePrefix="I Nostri "
        titleSuffix="Progetti"
      />


      <div v-if="loading" class="text-center py-20">
        <div class="relative inline-block">
          <div class="w-16 h-16 rounded-full border-4 border-red/30 animate-spin"></div>
          <div class="w-16 h-16 rounded-full border-t-4 border-red absolute top-0 left-0 animate-spin-fast"></div>
        </div>
        <p class="mt-6 text-gray-500">Caricamento progetti in corso...</p>
      </div>

      <div v-else-if="error" class="text-center py-16 transform transition-all duration-500 animate-fadeIn">
        <div class="p-8 rounded-xl bg-white shadow-lg max-w-xl mx-auto">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto mb-4 text-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <p class="text-xl text-gray-700">{{ error }}</p>
          <button @click="fetchProjects" class="mt-4 px-4 py-2 bg-red text-white rounded-md hover:bg-red-700 transition-colors">
            Riprova
          </button>
        </div>
      </div>

      <div v-else-if="projects.length === 0" class="text-center py-16 animate-fadeIn">
        <div class="p-8 rounded-xl bg-white shadow-lg max-w-xl mx-auto">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto mb-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          </svg>
          <p class="text-xl text-gray-500">Nessun progetto disponibile al momento.</p>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
        <div
          v-for="(project, index) in projects"
          :key="project.id"
          class="bg-white rounded-xl overflow-hidden shadow-lg group hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2"
          :style="{ transitionDelay: index * 100 + 'ms' }"
          :class="{ 'opacity-0 translate-y-10': loading, 'opacity-100 translate-y-0': !loading }"
        >
          <div class="relative h-64 overflow-hidden">
            <img
              v-if="project.thumbnail_url"
              :src="getImageUrl(project.thumbnail_url)"
              :alt="project.name"
              class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            >
            <div v-else class="w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <!-- Overlay per effetto hover migliorato -->
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

            <!-- Bordo animato al hover -->
            <div class="absolute inset-0 border-0 border-red/0 group-hover:border-2 group-hover:border-red/70 transition-all duration-300 rounded-t-xl opacity-0 group-hover:opacity-100"></div>
          </div>

          <div class="p-8 relative">
            <!-- Status badge -->
            <span class="absolute top-0 right-6 -translate-y-1/2 text-xs font-medium bg-red/10 text-red py-1 px-4 rounded-full shadow-sm">
              {{ project.status || 'In corso' }}
            </span>

            <h3 class="text-xl font-bold text-gray-800 group-hover:text-red transition-colors duration-300 mb-3">{{ project.name }}</h3>

            <p class="text-gray-600 mb-6 line-clamp-3">{{ project.description }}</p>

            <div class="pt-4 border-t border-gray-200">
              <router-link
                :to="{ name: 'ProjectDetail', params: { id: project.id }}"
                class="inline-flex items-center text-red hover:text-red-700 font-medium transition-all duration-300 group-hover:font-semibold"
              >
                Scopri di più
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2 transform group-hover:translate-x-2 transition-transform duration-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-center mt-8">
            <router-link
              to="/projects"
              class="w-64 flex items-center justify-center px-6 py-3 border-2 border-red text-red text-lg font-semibold rounded-lg text-center hover:border-[#0b2a63] hover:text-[#E7000B] shadow-lg transform transition-all duration-300 hover:scale-105 hover:bg-red-50"
            >
              Vedi tutti i Progetti
            </router-link>
          </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ApiService from '@/services/ApiService';
import SectionHeader from '@/components/ui/SectionHeader.vue';

const router = useRouter();
const projects = ref([]);
const loading = ref(true);
const error = ref(null);
const API_BASE_URL = ApiService.baseURL();

const getImageUrl = (thumbnailUrl) => {
  if (!thumbnailUrl) return null;

  // Se l'URL è già assoluto (inizia con http:// o https://)
  if (thumbnailUrl.startsWith('http://') || thumbnailUrl.startsWith('https://')) {
    return thumbnailUrl;
  }

  // Altrimenti, prependi l'URL base del backend
  return `${API_BASE_URL}${thumbnailUrl}`;
};

const fetchProjects = async () => {
  loading.value = true;
  error.value = null;

  try {
    const response = await ApiService.getProjects();
    projects.value = response.data;

    // Breve timeout per consentire l'animazione di caricamento
    setTimeout(() => {
      loading.value = false;
    }, 500);
  } catch (err) {
    error.value = 'Errore nel caricamento dei progetti. Riprova più tardi.';
    console.error('Error fetching projects:', err);
    loading.value = false;
  }
};

const ProjectsView = () => {
  router.push({ name: 'projects-list' });
};

onMounted(() => {
  fetchProjects();
});
</script>

<style scoped>
.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float-delayed {
  animation: float 8s ease-in-out 1s infinite;
}

.animate-pulse-slow {
  animation: pulse 6s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-fadeIn {
  animation: fadeIn 0.8s ease-out forwards;
}

.animate-spin-fast {
  animation: spin 0.8s linear infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.05;
  }
  50% {
    opacity: 0.1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
