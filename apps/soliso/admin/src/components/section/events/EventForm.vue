<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div class="mb-4">
      <label for="title" class="block text-gray-700 text-sm font-bold mb-2">Titolo Evento: *</label>
      <input type="text" id="title" v-model="eventData.title" required
        class="shadow border rounded w-full py-2 px-3 text-gray-700 focus:ring-2 focus:ring-blue-500" />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="mb-4">
        <label for="start_date" class="block text-gray-700 text-sm font-bold mb-2">Data Inizio: *</label>
        <input type="datetime-local" id="start_date" v-model="eventData.start_date" required
          class="shadow border rounded w-full py-2 px-3 text-gray-700 focus:ring-2 focus:ring-blue-500" />
      </div>

      <div class="mb-4">
        <label for="end_date" class="block text-gray-700 text-sm font-bold mb-2">Data Fine:</label>
        <input type="datetime-local" id="end_date" v-model="eventData.end_date"
          class="shadow border rounded w-full py-2 px-3 text-gray-700 focus:ring-2 focus:ring-blue-500" />
      </div>
    </div>

    <div class="mb-4">
      <label for="location" class="block text-gray-700 text-sm font-bold mb-2">Luogo:</label>
      <input type="text" id="location" v-model="eventData.location"
        class="shadow border rounded w-full py-2 px-3 text-gray-700 focus:ring-2 focus:ring-blue-500" />
    </div>

    <div class="mb-4">
      <label for="description" class="block text-gray-700 text-sm font-bold mb-2">Descrizione:</label>
      <textarea id="description" v-model="eventData.description" rows="4"
        class="shadow border rounded w-full py-2 px-3 text-gray-700 focus:ring-2 focus:ring-blue-500"></textarea>
    </div>

    <div class="mb-4">
      <label for="image" class="block text-gray-700 text-sm font-bold mb-2">Immagine Evento:</label>
      <div class="flex flex-col space-y-2">
        <div v-if="isEditing && eventData.image_url && !imagePreview" class="mb-2">
          <p class="text-sm text-gray-600 mb-1">Immagine attuale:</p>
          <EventImage :image-url="eventData.image_url" :alt-text="eventData.title" size="150x150" />
        </div>

        <div v-if="imagePreview" class="mb-2">
          <p class="text-sm text-gray-600 mb-1">Anteprima immagine:</p>
          <div class="relative w-full max-w-xs">
            <img :src="imagePreview" alt="Anteprima immagine" class="h-40 object-cover rounded border border-gray-300" />
            <button @click="clearImageSelection" type="button"
              class="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 hover:bg-red-700 transition">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div class="flex flex-col">
          <input type="file" id="image" @change="handleFileUpload" accept="image/*"
            class="w-full text-gray-700 border rounded py-2 px-3 focus:ring-2 focus:ring-blue-500" />
          <p class="text-xs text-gray-500 mt-1">Formati supportati: JPG, PNG, GIF (max 5MB)</p>
        </div>
      </div>
    </div>

    <div class="mb-6">
      <label class="flex items-center">
        <input type="checkbox" v-model="eventData.is_featured" class="form-checkbox h-5 w-5 text-blue-600">
        <span class="ml-2 text-gray-700">Evento in evidenza</span>
      </label>
    </div>

    <div class="flex items-center justify-between">
      <BaseButton
        type="submit"
        :disabled="isSubmitting"
        variant="primary"
      >
        {{ isSubmitting ? 'Salvataggio...' : (isEditing ? 'Aggiorna Evento' : 'Crea Evento') }}
      </BaseButton>
      <router-link :to="{ name: 'events-list' }" class="text-blue-500 hover:underline font-bold text-sm">
        Annulla
      </router-link>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import ApiService from '../../../services/ApiService';
import EventImage from '../../ui/images/EventImage.vue';
import BaseButton from '../../common/BaseButton.vue';

const props = defineProps({
  isEditing: {
    type: Boolean,
    default: false
  },
  eventId: {
    type: Number,
    default: null
  }
});

const emit = defineEmits(['success', 'error']);

const router = useRouter();
const isSubmitting = ref(false);
const file = ref(null);
const imagePreview = ref(null);

const eventData = reactive({
  title: '',
  description: '',
  start_date: '',
  end_date: '',
  location: '',
  image_url: null,
  is_featured: false
});

const handleFileUpload = (event) => {
  const selectedFile = event.target.files[0];
  if (selectedFile) {
    if (selectedFile.size > 5 * 1024 * 1024) {
      emit('error', 'La dimensione dell\'immagine supera il limite di 5MB. Seleziona un\'immagine più piccola.');
      event.target.value = '';
      return;
    }

    file.value = selectedFile;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target.result;
    };
    reader.readAsDataURL(selectedFile);
  }
};

const clearImageSelection = () => {
  file.value = null;
  imagePreview.value = null;
  const fileInput = document.getElementById('image');
  if (fileInput) fileInput.value = '';
};

const fetchEventData = async () => {
  if (!props.isEditing || !props.eventId) return;

  try {
    const response = await ApiService.getEvent(props.eventId);
    const data = response.data;
    Object.assign(eventData, {
      title: data.title,
      description: data.description || '',
      start_date: data.start_date || '',
      end_date: data.end_date || '',
      location: data.location || '',
      image_url: data.image_url || null,
      is_featured: data.is_featured
    });
  } catch (err) {
    console.error("Impossibile recuperare i dati dell'evento:", err);
    if (err.response?.status === 404) {
      emit('error', 'Evento non trovato. Torna alla lista degli eventi e riprova.');
    } else {
      emit('error', err.response?.data?.detail || 'Impossibile caricare i dati dell\'evento.');
    }
  }
};

const validateDates = () => {
  if (eventData.end_date && eventData.start_date) {
    const startDate = new Date(eventData.start_date);
    const endDate = new Date(eventData.end_date);

    if (endDate < startDate) {
      emit('error', 'La data di fine deve essere successiva alla data di inizio.');
      return false;
    }
  }
  return true;
};

const handleSubmit = async () => {
  if (!eventData.title.trim()) {
    emit('error', 'Il titolo dell\'evento è obbligatorio.');
    return;
  }

  if (!eventData.start_date) {
    emit('error', 'La data di inizio è obbligatoria.');
    return;
  }

  if (!validateDates()) {
    return;
  }

  isSubmitting.value = true;

  try {
    const formData = new FormData();

    // Campi obbligatori
    formData.append('title', eventData.title.trim());
    formData.append('is_featured', eventData.is_featured);
    formData.append('start_date', eventData.start_date);

    // Campi opzionali
    if (eventData.description?.trim()) {
      formData.append('description', eventData.description.trim());
    }

    if (eventData.end_date) {
      formData.append('end_date', eventData.end_date);
    }

    if (eventData.location?.trim()) {
      formData.append('location', eventData.location.trim());
    }

    // Gestione immagine
    if (file.value) {
      formData.append('image', file.value);
    }

    // Logging di debug
    console.log('=== INFO DEBUG ===');
    console.log('Titolo:', eventData.title);
    console.log('Data Inizio:', eventData.start_date);
    console.log('Data Fine:', eventData.end_date);
    console.log('Luogo:', eventData.location);
    console.log('Descrizione:', eventData.description);
    console.log('In Evidenza:', eventData.is_featured);
    console.log('Ha Immagine:', !!file.value);
    if (file.value) {
      console.log('Dettagli Immagine:', {
        nome: file.value.name,
        tipo: file.value.type,
        dimensione: file.value.size
      });
    }

    const response = props.isEditing
      ? await ApiService.updateEvent(props.eventId, formData)
      : await ApiService.createEvent(formData);

    emit('success', response.data);
    router.push({ name: 'events-list' });
  } catch (err) {
    // Logging errori
    console.log('=== INFO ERRORE ===');
    console.log('Stato Errore:', err.response?.status);
    console.log('Dati Errore:', JSON.stringify(err.response?.data, null, 2));

    let errorMessage = 'Impossibile salvare l\'evento. Controlla i dati inseriti.';

    if (err.response?.data?.detail) {
      if (Array.isArray(err.response.data.detail)) {
        errorMessage = err.response.data.detail.join(', ');
      } else if (typeof err.response.data.detail === 'string') {
        errorMessage = err.response.data.detail;
      } else if (typeof err.response.data.detail === 'object') {
        errorMessage = Object.entries(err.response.data.detail)
          .map(([key, value]) => `${key}: ${value}`)
          .join(', ');
      }
    }

    emit('error', errorMessage);
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(fetchEventData);
</script>
