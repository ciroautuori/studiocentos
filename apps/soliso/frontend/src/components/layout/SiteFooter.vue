<template>
  <footer class="bg-gray-900 py-12 text-white">
    <div class="container mx-auto px-4">
      <div class="grid md:grid-cols-3 gap-8 mb-8">
        <div>
          <div class="text-2xl font-bold mb-4">SOL.I.<span class="text-red-500">SO</span></div>
          <p class="text-gray-300">
            Promuoviamo inclusione e solidarietà, creando connessioni per una società senza
            barriere.
          </p>
        </div>
        <div>
          <h4 class="text-xl font-bold mb-4">Link Utili</h4>
          <ul class="space-y-2">
            <li v-for="(link, index) in usefulLinks" :key="index">
              <router-link
                :to="link.url"
                class="text-gray-300 hover:text-red-500 transition-colors duration-300 inline-flex items-center group"
              >
                {{ link.text }}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4 ml-2 transform group-hover:translate-x-1 transition-transform duration-300"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </router-link>
            </li>
          </ul>
        </div>
        <div>
          <h4 class="text-xl font-bold mb-4">Contatti</h4>
          <div class="space-y-4">
            <a href="tel:+393895381678" class="flex items-center text-gray-300 hover:text-red-500 transition-colors duration-300 group">
              <div class="w-10 h-10 rounded-full bg-blue-800 flex items-center justify-center mr-3 group-hover:bg-red-500/30 transition-colors duration-300">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                </svg>
              </div>
              {{ contactInfo.phone }}
            </a>
            <a href="mailto:associazionesoliso@gmail.com" class="flex items-center text-gray-300 hover:text-red-500 transition-colors duration-300 group">
              <div class="w-10 h-10 rounded-full bg-blue-800 flex items-center justify-center mr-3 group-hover:bg-red-500/30 transition-colors duration-300">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                </svg>
              </div>
              {{ contactInfo.email }}
            </a>
            <div class="flex space-x-3 mt-6">
              <a
                v-for="(social, index) in socialLinks"
                :key="index"
                :href="social.url"
                target="_blank"
                rel="noopener noreferrer"
                class="w-10 h-10 rounded-full bg-blue-800 flex items-center justify-center text-white hover:bg-red-500 transition-all duration-300 transform hover:scale-110 hover:rotate-12"
              >
                <component :is="social.component" class="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>
      </div>
      <div class="border-t border-red-500 pt-8 text-center text-gray-300">
        <p class="mb-2">Partita IVA: {{ companyInfo.vatNumber }} | Pec: {{ companyInfo.pec }}</p>
        <p>&copy; {{ currentYear }} SOL.I.SO. Tutti i diritti riservati.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref, computed, h } from 'vue';

const usefulLinks = ref([
  { text: 'Chi Siamo', url: '/about' },
  { text: 'Progetti', url: '/projects' },
  { text: 'Eventi', url: '/events' },
]);

const contactInfo = ref({
  phone: '+39 389 53 81 678',
  email: 'associazionesoliso@gmail.com'
});

// Componenti per le icone social (SVG incorporati anziché dipendere da FontAwesome)
const FacebookIcon = () => h('svg', {
  xmlns: 'http://www.w3.org/2000/svg',
  viewBox: '0 0 320 512',
  fill: 'currentColor'
}, [
  h('path', { d: 'M279.14 288l14.22-92.66h-88.91v-60.13c0-25.35 12.42-50.06 52.24-50.06h40.42V6.26S260.43 0 225.36 0c-73.22 0-121.08 44.38-121.08 124.72v70.62H22.89V288h81.39v224h100.17V288z' })
]);

const InstagramIcon = () => h('svg', {
  xmlns: 'http://www.w3.org/2000/svg',
  viewBox: '0 0 448 512',
  fill: 'currentColor'
}, [
  h('path', { d: 'M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z' })
]);

const YoutubeIcon = () => h('svg', {
  xmlns: 'http://www.w3.org/2000/svg',
  viewBox: '0 0 576 512',
  fill: 'currentColor'
}, [
  h('path', { d: 'M549.655 124.083c-6.281-23.65-24.787-42.276-48.284-48.597C458.781 64 288 64 288 64S117.22 64 74.629 75.486c-23.497 6.322-42.003 24.947-48.284 48.597-11.412 42.867-11.412 132.305-11.412 132.305s0 89.438 11.412 132.305c6.281 23.65 24.787 41.5 48.284 47.821C117.22 448 288 448 288 448s170.78 0 213.371-11.486c23.497-6.321 42.003-24.171 48.284-47.821 11.412-42.867 11.412-132.305 11.412-132.305s0-89.438-11.412-132.305zm-317.51 213.508V175.185l142.739 81.205-142.739 81.201z' })
]);

const socialLinks = ref([
  {
    platform: 'facebook',
    url: 'https://www.facebook.com/associazione_soliso',
    component: FacebookIcon
  },
  {
    platform: 'instagram',
    url: 'https://www.instagram.com/soliso.italia/',
    component: InstagramIcon
  },
  {
    platform: 'youtube',
    url: 'https://www.youtube.com/@associazione_soliso',
    component: YoutubeIcon
  }
]);

const companyInfo = ref({
  vatNumber: '95155490659',
  pec: 'sol.i.so23@pec.it'
});

const currentYear = computed(() => new Date().getFullYear());
</script>