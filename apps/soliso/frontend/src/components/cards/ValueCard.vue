<template>
  <div class="bg-white p-6 rounded-xl shadow-custom hover:shadow-xl transition">
    <div class="text-3xl font-bold text-primary mb-4">{{ letter }}</div>
    <h4 class="font-bold mb-2">{{ title }}</h4>
    <p class="text-secondary">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  letter: {
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
  }
});
</script>
