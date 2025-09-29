<template>
  <div class="text-controller inline-flex items-center bg-gray-100 rounded-lg overflow-hidden p-0.5">
    <button
      @click="decreaseFontSize"
      class="flex items-center justify-center h-8 w-8 transition-colors"
      :class="[
        fontSize <= minFontSize
          ? 'text-gray-400 cursor-not-allowed'
          : 'text-gray-700 hover:bg-white hover:text-red-600 active:bg-white'
      ]"
      :disabled="fontSize <= minFontSize"
      title="Riduci dimensione testo"
    >
      <span class="text-sm font-medium">A</span>
      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" clip-rule="evenodd" />
      </svg>
    </button>

    <div class="text-xs text-gray-500 px-1.5">
      {{ fontSize }}px
    </div>

    <button
      @click="increaseFontSize"
      class="flex items-center justify-center h-8 w-8 transition-colors"
      :class="[
        fontSize >= maxFontSize
          ? 'text-gray-400 cursor-not-allowed'
          : 'text-gray-700 hover:bg-white hover:text-red-600 active:bg-white'
      ]"
      :disabled="fontSize >= maxFontSize"
      title="Aumenta dimensione testo"
    >
      <span class="text-sm font-medium">A</span>
      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';

// Configurazione
const minFontSize = 14;
const maxFontSize = 24;
const step = 2;
const storageKey = 'app-font-size';

// Stato
const fontSize = ref(16);

// Carica la dimensione del font iniziale
onMounted(() => {
  // Recupera dalla localStorage se disponibile
  const savedFontSize = localStorage.getItem(storageKey);
  if (savedFontSize) {
    fontSize.value = parseInt(savedFontSize);
  }

  // Applica la dimensione del font al caricamento
  applyFontSize();

  // Aggiungi classe di transizione al body per rendere fluido il cambio di dimensione
  document.body.classList.add('font-transition');
});

// Rimuovi la classe di transizione quando il componente viene smontato
onUnmounted(() => {
  document.body.classList.remove('font-transition');
});

// Osserva i cambiamenti nella dimensione del font e applica le modifiche
watch(fontSize, (newSize) => {
  // Salva nella localStorage
  localStorage.setItem(storageKey, newSize.toString());

  // Applica al DOM
  applyFontSize();
});

// Aumenta la dimensione del font
const increaseFontSize = () => {
  if (fontSize.value < maxFontSize) {
    fontSize.value += step;
  }
};

// Diminuisci la dimensione del font
const decreaseFontSize = () => {
  if (fontSize.value > minFontSize) {
    fontSize.value -= step;
  }
};

// Applica la dimensione del font al documento
const applyFontSize = () => {
  document.documentElement.style.fontSize = `${fontSize.value}px`;

  // Aggiornamento variabili CSS per componenti che potrebbero usare rem
  document.documentElement.style.setProperty('--base-font-size', `${fontSize.value / 16}rem`);
};
</script>

<style>
/* Aggiungi al tuo CSS globale o importalo */
.font-transition {
  transition: font-size 0.3s ease;
}

:root {
  --base-font-size: 1rem;
}
</style>
