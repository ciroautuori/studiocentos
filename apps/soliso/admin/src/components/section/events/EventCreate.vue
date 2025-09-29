<template>
  <div class="bg-white p-3 sm:p-4 md:p-6 rounded-lg shadow max-w-lg mx-auto">
    <PageHeader title="Create New Event" />

    <div v-if="error" class="text-red-500 bg-red-100 p-3 sm:p-4 rounded-lg mb-4">{{ error }}</div>

    <EventForm
      :is-editing="false"
      @success="handleSuccess"
      @error="handleError"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import PageHeader from '../../../components/ui/headers/PageHeader.vue';
import EventForm from '../../../components/section/events/EventForm.vue';

const error = ref(null);

const handleSuccess = (data) => {
  console.log('event created successfully:', data);
};

const handleError = (message) => {
  error.value = message;
};
</script>
