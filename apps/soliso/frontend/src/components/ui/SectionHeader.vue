<template>
  <div class="text-center mb-20 transform transition-all duration-700" :class="{'opacity-100 translate-y-0': !loading, 'opacity-0 translate-y-10': loading}">
    <h6 class="inline-block px-3 py-1 text-red-600 font-semibold tracking-wider text-sm rounded-full bg-red-600/10 uppercase mb-3 animate-fadeIn">{{ label }}</h6>
    <h2 class="text-3xl md:text-5xl font-bold mb-6 text-gray-800 relative inline-block group">
      {{ titlePrefix }} <span class="text-red-600 relative">
        {{ titleSuffix }}
        <span class="absolute -bottom-1 left-0 w-full h-1 bg-red-600 scale-x-100 group-hover:scale-x-0 transition-transform duration-300 origin-right"></span>
        <span class="absolute -bottom-1 left-0 w-full h-1 bg-[#0b2a63] scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"></span>
      </span>
    </h2>
    <p class="text-gray-600 text-lg max-w-3xl mx-auto">{{ subtitle }}</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

// Definisco le props con valori predefiniti
defineProps({
  label: {
    type: String,
    default: 'Progetti' // Puoi modificare il valore predefinito se necessario
  },
  titlePrefix: {
    type: String,
    default: 'Le Nostre' // La parte dinamica del titolo
  },
  titleSuffix: {
    type: String,
    default: 'Iniziative' // La parte dinamica del titolo
  },
  subtitle: {
    type: String,
    default: 'Scopri le iniziative e i progetti su cui stiamo lavorando per fare la differenza nella nostra comunità.'
  },
  loading: {
    type: Boolean,
    default: false
  }
});
</script>
