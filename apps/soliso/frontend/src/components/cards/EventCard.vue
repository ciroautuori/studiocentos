<template>
  <div class="bg-white rounded-2xl shadow-custom hover:shadow-xl transition p-8">
    <div class="text-primary font-bold mb-4">{{ date }}</div>
    <div>
      <h4 class="text-xl font-bold mb-2">{{ title }}</h4>
      <p class="text-secondary mb-2">{{ description }}</p>
      <p class="text-gray-500">Luogo: {{ location }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  date: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  location: {
    type: String,
    required: true
  }
});
</script>
