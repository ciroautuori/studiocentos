<template>
  <section id="contatti" class="py-24 relative overflow-hidden bg-red-600/5">
    <!-- Elementi decorativi di sfondo -->
    <div class="absolute -top-20 -left-20 w-96 h-96 rounded-full bg-red-600/10"></div>
    <div class="absolute -bottom-32 -right-16 w-80 h-80 rounded-full bg-[#0b2a63]/10"></div>

    <div class="container mx-auto px-4 relative z-10">
      <SectionHeader
        title="Contattaci"
        titlePrefix="Siamo qui per "
        titleSuffix="aiutarti"
        titleHighlight="Contatti"
        subtitle="Contattaci per maggiori informazioni o per unirti alla nostra causa."
        label="Contatti"
      />

      <div class="grid md:grid-cols-2 gap-12 mt-12">
        <!-- Primo box con informazioni di contatto -->
        <div class="bg-white rounded-xl shadow-xl p-8 transform transition-all duration-300 hover:shadow-lg hover:scale-105 group">
          <h3 class="text-2xl font-bold mb-6 text-gray-800 group-hover:text-[#0b2a63] transition-colors duration-300">Restiamo in Contatto</h3>
          <p class="text-gray-600 mb-8">
            Per informazioni, collaborazione o supporto, siamo a tua disposizione.
          </p>
          <div class="space-y-6">
            <div v-for="(info, index) in contactInfo" :key="index" class="flex items-start group/item">
              <div class="w-12 h-12 rounded-full bg-red-600 text-white flex items-center justify-center mr-4 flex-shrink-0 group-hover/item:bg-[#0b2a63] transition-colors duration-300">
                <font-awesome-icon :icon="info.icon" class="text-lg" />
              </div>
              <div>
                <h4 class="text-lg font-semibold mb-1 text-gray-800 group-hover/item:text-[#0b2a63] transition-colors duration-300">{{ info.title }}</h4>
                <p class="text-gray-600">{{ info.value }}</p>
              </div>
            </div>
          </div>

          <div class="mt-10 pt-8 border-t border-gray-100">
            <h4 class="text-lg font-semibold mb-4 text-gray-800 group-hover:text-[#0b2a63] transition-colors duration-300">Seguici sui Social</h4>
            <div class="flex space-x-4">
              <a
                v-for="social in socialLinks"
                :key="social.platform"
                :href="social.url"
                target="_blank"
                rel="noopener noreferrer"
                class="w-12 h-12 rounded-full bg-red-600 flex items-center justify-center text-white hover:bg-[#0b2a63] transition-all duration-300 transform hover:scale-110 hover:rotate-12 group/social"
              >
                <font-awesome-icon :icon="['fab', social.icon]" class="text-xl transition-transform duration-300 group-hover/social:scale-110" />
              </a>
            </div>
          </div>
        </div>

        <!-- Secondo box con il form di contatto -->
        <div class="bg-white rounded-xl shadow-xl p-8 transform transition-all duration-300 hover:shadow-lg hover:scale-105 group">
          <h3 class="text-2xl font-bold mb-6 text-gray-800 group-hover:text-[#0b2a63] transition-colors duration-300">Invia un Messaggio</h3>
          <ContactForm />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import SectionHeader from '../ui/SectionHeader.vue';
import ContactForm from '../contact/ContactForm.vue';
import { faPhone, faEnvelope, faLocationDot } from '@fortawesome/free-solid-svg-icons';

const contactInfo = ref([
  {
    icon: faPhone,
    title: 'Telefono',
    value: '+39 389 53 81 678'
  },
  {
    icon: faEnvelope,
    title: 'Email',
    value: 'associazionesoliso@gmail.com'
  },
  {
    icon: faLocationDot,
    title: 'Indirizzo',
    value: 'Via Madonna Del Monte, 33 - Salerno'
  }
]);

const socialLinks = ref([
  { platform: 'facebook', url: 'https://www.facebook.com/AssociazioneSoliso?locale=it_IT', icon: 'facebook-f' },
  { platform: 'instagram', url: 'https://www.instagram.com/associazionesoliso/', icon: 'instagram' },
  { platform: 'youtube', url: '#', icon: 'youtube' }
]);
</script>
