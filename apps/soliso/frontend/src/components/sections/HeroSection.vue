<template>
  <section class="relative min-h-screen flex items-center justify-center overflow-hidden group">
    <!-- Background con immagine -->
    <div
      class="absolute inset-0 z-0 transition-all duration-500"
      :style="`background-image: url('${heroBg}'); background-size: cover; background-position: center;`"
    ></div>
    <!-- Overlay blu in hover -->
    <div class="absolute inset-0 z-10 bg-blue-700/40 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
    <!-- Overlay gradient sopra l'immagine -->
    <div class="absolute inset-0 z-20 bg-gradient-to-r from-gray-900 to-gray-800 opacity-80"></div>

    <!-- Cerchi decorativi di sfondo -->
    <div class="absolute -top-20 -left-20 w-96 h-96 rounded-full bg-red opacity-10 z-30"></div>
    <div class="absolute -bottom-32 -right-16 w-80 h-80 rounded-full bg-blue opacity-10 z-30"></div>

    <!-- Elementi decorativi di sfondo -->
    <div class="absolute top-0 left-0 w-1/3 h-full bg-red-600/10 skew-x-12 transform origin-top-left"></div>
    <div class="absolute bottom-0 right-0 w-96 h-96 rounded-full bg-[#0b2a63]/10 blur-3xl"></div>

    <!-- Contenuto -->
    <div class="container mx-auto px-4 relative z-30 py-20">
      <div class="max-w-4xl mx-auto text-center">
        <!-- Titolo con animazione -->
        <h1 class="text-4xl md:text-6xl font-bold mb-6 text-white leading-tight">
          Abbattiamo le <span class="relative">
            barriere
            <span class="absolute bottom-0 left-0 w-full h-1 bg-red"></span>
          </span><br />
          Costruiamo <span class="text-red">Inclusione</span>.
        </h1>

        <!-- Sottotitolo -->
        <p class="text-xl text-gray-200 mb-10 max-w-3xl mx-auto">
          SOL.I.SO promuove l'inclusione sociale delle persone sorde attraverso educazione,
          cultura e sensibilizzazione. Insieme per una società senza barriere.
        </p>

        <!-- Call to action buttons -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <a
            :href="primaryCta.link"
            class="btn-red px-8 py-4 rounded-lg font-semibold text-lg shadow-lg transform transition-all duration-300 hover:scale-105 hover:shadow-xl"
          >
            {{ primaryCta.text }}
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2 inline" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H3a1 1 0 110-2h9.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </a>
          <a
            :href="secondaryCta.link"
            class="bg-transparent border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg shadow-lg transform transition-all duration-300 hover:scale-105 hover:bg-white/10"
          >
            {{ secondaryCta.text }}
          </a>
        </div>
      </div>
    </div>

    <!-- Freccia scorri in basso -->
    <div class="absolute bottom-10 left-1/2 transform -translate-x-1/2 animate-bounce z-30">
      <a href="#chi-siamo" class="text-white opacity-70 hover:opacity-100 transition-opacity">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </a>
    </div>
  </section>
</template>

<script setup>
import { defineProps } from 'vue';
import heroBg from '@/assets/img/hero.jpg';

defineProps({
  primaryCta: {
    type: Object,
    default: () => ({
      text: 'Scopri i Nostri Servizi',
      link: '#servizi'
    })
  },
  secondaryCta: {
    type: Object,
    default: () => ({
      text: 'Chi Siamo',
      link: '/about'
    })
  }
});
</script>
