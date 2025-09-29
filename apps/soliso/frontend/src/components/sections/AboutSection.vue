<template>
  <section id="chi-siamo" class="py-24 relative overflow-hidden bg-[#0b2a63]/5">
    <!-- Elementi decorativi di sfondo -->
    <div
      class="absolute top-0 right-0 w-1/3 h-full bg-[#0b2a63]/10 -skew-x-12 transform origin-top-right"
    ></div>
    <div class="absolute bottom-0 left-0 w-96 h-96 rounded-full bg-red-600/10 blur-3xl"></div>

    <div class="container mx-auto px-4 relative z-10">
      <SectionHeader
        title="Chi Siamo"
        titleHighlight="SOL.I.SO"
        subtitle="Un team dedicato all'inclusione e alla comunicazione."
        label="Chi Siamo"
        titlePrefix="La Nostra "
        titleSuffix="Storia"
      />

      <div class="grid lg:grid-cols-2 gap-8 lg:gap-16 items-center mt-8 lg:mt-16">
        <!-- Modern image section with hover effects -->
        <div class="relative group max-w-[500px] mx-auto lg:mx-0 w-full">
          <!-- Image container with modern effects -->
          <div
            class="relative rounded-lg overflow-hidden shadow-lg transform group-hover:scale-[1.01] transition-all duration-300"
          >
            <div class="aspect-[3/4] sm:aspect-[4/3] w-full relative">
              <img
                :src="sorelleImage"
                alt="Il team di SOL.I.SO"
                class="absolute inset-0 w-full h-full object-cover"
              />
              <!-- Modern gradient overlay -->
              <div
                class="absolute inset-0 bg-gradient-to-t from-gray-900/80 to-transparent opacity-0 group-hover:opacity-100 transition-all duration-300"
              ></div>

              <!-- Hover content -->
              <div
                class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              >
                <div
                  class="text-center text-white transform translate-y-2 group-hover:translate-y-0 transition-transform duration-300"
                >
                  <h3 class="text-xl lg:text-2xl font-bold mb-1">Il Nostro Team</h3>
                  <p class="text-sm text-gray-200">Scopri di più su di noi</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Decorative elements -->
          <div
            class="absolute -bottom-2 -right-2 w-16 h-16 bg-red/20 rounded-full blur-lg opacity-0 group-hover:opacity-100 transition-all duration-300"
          ></div>
          <div
            class="absolute -top-2 -left-2 w-16 h-16 bg-blue/20 rounded-full blur-lg opacity-0 group-hover:opacity-100 transition-all duration-300"
          ></div>
        </div>

        <!-- Text column with centered content on mobile -->
        <div class="text-center lg:text-left">
          <h3 class="text-3xl font-bold mb-6 text-gray-800">La Nostra Storia</h3>
          <p class="text-lg text-gray-600 leading-relaxed mb-8">
            Fondata nel 2009 da professionisti e appassionati, SOL.I.SO nasce con l'obiettivo di
            superare le barriere comunicative e culturali. Collaboriamo con istituzioni e scuole per
            promuovere una cultura inclusiva.
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div
              v-for="(value, index) in values"
              :key="index"
              class="group p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-t-4 border-red hover:border-red-600 transform hover:-translate-y-1"
            >
              <div
                class="w-12 h-12 rounded-xl bg-red/10 flex items-center justify-center mb-4 text-red font-bold text-xl group-hover:bg-red/20 transition-colors duration-300"
              >
                {{ value.letter }}
              </div>
              <h4
                class="text-xl font-semibold mb-3 text-gray-800 group-hover:text-red transition-colors duration-300"
              >
                {{ value.title }}
              </h4>
              <p class="text-gray-600">{{ value.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import SectionHeader from '../ui/SectionHeader.vue'
import sorelleImage from '@/assets/img/sorelle.jpg'

// Add custom animation
const style = document.createElement('style')
style.textContent = `
  @keyframes spin-slow {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  .animate-spin-slow {
    animation: spin-slow 20s linear infinite;
  }
`
document.head.appendChild(style)

const values = ref([
  {
    letter: 'E',
    title: 'Educazione',
    description: 'Diffondiamo la Lingua dei Segni Italiana e la cultura sorda.',
  },
  {
    letter: 'I',
    title: 'Inclusione',
    description:
      'Lavoriamo per abbattere le barriere comunicative e creare una società accessibile.',
  },
  {
    letter: 'C',
    title: 'Comunità',
    description: 'Creiamo spazi di incontro e confronto per rafforzare il senso di appartenenza.',
  },
])
</script>
