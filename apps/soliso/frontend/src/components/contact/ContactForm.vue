<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <!-- Campo Nome -->
    <div class="grid md:grid-cols-2 gap-6">
      <div class="form-group">
        <label for="name" class="block text-sm font-medium text-gray-700 mb-1">Nome</label>
        <input id="name" v-model.trim="form.name" type="text"
          class="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-all duration-300"
          placeholder="Il tuo nome" required aria-required="true" />
      </div>

      <!-- Campo Email -->
      <div class="form-group">
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input id="email" v-model.trim="form.email" type="email"
          class="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-all duration-300"
          placeholder="La tua email" required aria-required="true" />
      </div>
    </div>

    <!-- Campo Oggetto -->
    <div class="form-group">
      <label for="subject" class="block text-sm font-medium text-gray-700 mb-1">Oggetto</label>
      <input id="subject" v-model.trim="form.subject" type="text"
        class="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-all duration-300"
        placeholder="Oggetto del messaggio" required aria-required="true" />
    </div>

    <!-- Campo Messaggio -->
    <div class="form-group">
      <label for="message" class="block text-sm font-medium text-gray-700 mb-1">Messaggio</label>
      <textarea id="message" v-model.trim="form.message" rows="5"
        class="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-all duration-300"
        placeholder="Scrivi il tuo messaggio qui" required aria-required="true"></textarea>
    </div>

    <!-- Campo Privacy -->
    <div class="form-group">
      <label class="relative flex items-start p-4 bg-gray-50 rounded-lg border border-gray-200 hover:border-red-200 transition-all duration-300 cursor-pointer group">
        <div class="flex items-center h-5">
          <input v-model="form.privacy" type="checkbox"
            class="w-4 h-4 text-red-600 border-gray-300 rounded focus:ring-red-500 transition-all duration-300 peer"
            required aria-required="true" />
          <div class="absolute w-4 h-4 border-2 border-gray-300 rounded transition-all duration-300 peer-checked:border-red-600 peer-checked:bg-red-600 group-hover:border-red-300"></div>
          <div class="absolute w-4 h-4 flex items-center justify-center opacity-0 peer-checked:opacity-100 transition-opacity duration-300">
            <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
        </div>
        <div class="ml-3 text-sm">
          <span class="text-gray-600 group-hover:text-gray-900 transition-colors duration-300">
            Ho letto e accetto la
            <a href="/privacy-policy" target="_blank" rel="noopener noreferrer"
              class="text-red-600 hover:text-red-700 font-medium hover:underline transition-colors duration-300">
              Privacy Policy
            </a>
          </span>
        </div>
      </label>
    </div>

    <!-- Bottone Submit -->
    <div class="flex justify-end">
      <button type="submit"
        class="px-6 py-3 bg-red-600 text-white font-medium rounded-md shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-opacity-50 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="loading" aria-label="Invia il messaggio del modulo di contatto">
        <span v-if="loading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24" aria-hidden="true"> <!-- Aggiunto aria-hidden -->
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
          </svg>
          Invio in corso...
        </span>
        <span v-else>Invia Messaggio</span>
      </button>
    </div>

    <!-- Messaggio di Stato -->
    <div v-if="formStatus.show"
      :class="`p-4 rounded-md ${formStatus.error ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`"
      role="status" aria-live="polite">
      {{ formStatus.message }}
    </div>
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue';

// Stato reattivo del modulo
const form = reactive({
  name: '',
  email: '',
  subject: '',
  message: '',
  privacy: false
});

// Stato per indicare il caricamento durante l'invio
const loading = ref(false);

// Stato per mostrare messaggi di successo o errore
const formStatus = reactive({
  show: false,
  error: false,
  message: ''
});

// Funzione per resettare il modulo ai valori iniziali
const resetForm = () => {
  form.name = '';
  form.email = '';
  form.subject = '';
  form.message = '';
  form.privacy = false;
  // Alternativa più concisa se si vuole resettare TUTTO l'oggetto form:
  // Object.assign(form, { name: '', email: '', subject: '', message: '', privacy: false });
};

// Funzione asincrona per gestire l'invio del modulo
const submitForm = async () => {
  loading.value = true;
  formStatus.show = false; // Nasconde messaggi precedenti

  try {
    // --- SIMULAZIONE CHIAMATA API ---
    // Sostituisci questa parte con la tua logica di invio reale (es. fetch, axios)
    console.log('Invio dati modulo:', JSON.stringify(form));
    await new Promise(resolve => setTimeout(resolve, 1500)); // Simula attesa di 1.5 secondi
    // --- Fine Simulazione ---

    // Verifica simulata di successo (in un caso reale, dipenderebbe dalla risposta API)
    const success = true; // Cambia a false per testare l'errore

    if (success) {
      // Reset del form dopo invio riuscito
      resetForm();

      // Imposta messaggio di successo
      formStatus.error = false;
      formStatus.message = 'Messaggio inviato con successo! Ti risponderemo al più presto.';
      formStatus.show = true;
    } else {
      // Simula un errore dall'API
      throw new Error('Errore simulato durante l\'invio.');
    }

  } catch (error) {
    console.error('Errore durante l\'invio del modulo:', error); // Logga l'errore effettivo in console

    // Imposta messaggio di errore
    formStatus.error = true;
    formStatus.message = 'Si è verificato un errore durante l\'invio del messaggio. Riprova più tardi.';
    // Potresti mostrare un messaggio più specifico basato su `error` se disponibile
    // formStatus.message = `Errore: ${error.message || 'Riprova più tardi.'}`;
    formStatus.show = true;
  } finally {
    // Assicura che lo stato di caricamento venga disattivato in ogni caso
    loading.value = false;
  }
};

</script>
