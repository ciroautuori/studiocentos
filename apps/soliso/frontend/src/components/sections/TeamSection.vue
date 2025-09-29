<template>
  <section id="team" class="py-24 bg-gradient-to-b from-gray-50 to-white relative overflow-hidden">
    <!-- Elementi decorativi di sfondo -->
    <div class="absolute top-0 right-0 w-1/3 h-full bg-red-600/5 -skew-x-12 transform origin-top-right"></div>
    <div class="absolute bottom-0 left-0 w-96 h-96 rounded-full bg-[#0b2a63]/5 blur-3xl"></div>

    <div class="container mx-auto px-4 relative z-10">
      <SectionHeader
        title="Il Nostro "
        titleHighlight="Team"
        subtitle="Il nostro team di esperti e appassionati, uniti dalla voglia di fare la differenza."
        label="Team"
        titlePrefix="Il Nostro "
        titleSuffix="Team"
      />

      <div class="grid md:grid-cols-2 gap-12 mt-16">
        <div
          v-for="(member, index) in teamMembers"
          :key="index"
          class="group"
        >
          <!-- Card principale -->
          <div class="bg-white rounded-3xl overflow-hidden shadow-xl group-hover:shadow-2xl transition-all duration-500 hover:scale-[1.02] hover:-translate-y-2">
            <!-- Contenuto -->
            <div class="p-8">
              <div class="flex flex-col items-center text-center mb-6">
                <div class="w-32 h-32 rounded-full border-4 border-red-600 bg-white shadow-lg overflow-hidden mb-4 group-hover:shadow-xl transition-all duration-500 group-hover:border-[#0b2a63]">
                  <img
                    :src="member.image"
                    :alt="member.name"
                    class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                  />
                </div>
                <h3 class="text-2xl font-bold text-gray-900 mb-2 group-hover:text-[#0b2a63] transition-colors duration-300">{{ member.name }}</h3>
                <p class="text-red-600 font-medium mb-4 group-hover:text-[#0b2a63] transition-colors duration-300">{{ member.role }}</p>
              </div>

              <p class="text-gray-600 leading-relaxed mb-6 text-center group-hover:text-gray-800 transition-colors duration-300">{{ member.description }}</p>

              <!-- Social Links -->
              <div class="flex justify-center gap-4">
                <a
                  v-for="(link, i) in member.socialLinks"
                  :key="i"
                  :href="link.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="relative inline-flex items-center justify-center w-12 h-12 rounded-full bg-red-600 text-white hover:bg-[#0b2a63] transition-all duration-300 transform hover:scale-110 hover:rotate-12 group/social"
                >
                  <font-awesome-icon :icon="['fab', link.icon]" class="text-xl transition-transform duration-300 group-hover/social:scale-110" />
                  <span class="absolute -bottom-8 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white text-xs py-1 px-2 rounded opacity-0 group-hover/social:opacity-100 transition-opacity duration-300 whitespace-nowrap">
                    {{ link.platform }}
                  </span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import SectionHeader from '../ui/SectionHeader.vue';
import idaImage from '@/assets/img/Ida.jpg';
import luisaImage from '@/assets/img/Luisa.jpg';

const teamMembers = ref([
  {
    name: 'Ida Mautone',
    role: 'Presidente',
    description: 'Esperto in comunicazione e inclusione, guida il team con passione.',
    image: idaImage,
    socialLinks: [
      { platform: 'Facebook', url: 'https://www.facebook.com/ida.mautone.1?locale=it_IT', icon: 'facebook-f' },
      { platform: 'Instagram', url: 'https://www.instagram.com/idamautone/', icon: 'instagram' }
    ]
  },
  {
    name: 'Luisa Mautone',
    role: 'Coordinatore',
    description: 'Si occupa di relazioni esterne e di diffondere la mission dell\'associazione.',
    image: luisaImage,
    socialLinks: [
      { platform: 'Facebook', url: 'https://www.facebook.com/luisa.mautone.9?locale=it_IT', icon: 'facebook-f' },
      { platform: 'Instagram', url: 'https://www.instagram.com/mautoneluisa/', icon: 'instagram' }
    ]
  }
]);
</script>
