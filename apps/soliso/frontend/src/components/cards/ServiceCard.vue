<template>
  <div class="bg-white rounded-xl shadow-custom hover:shadow-xl transition overflow-hidden">
    <img
      :src="image"
      :alt="imageAlt"
      class="w-full h-64 object-cover"
    />
    <div class="p-8">
      <h4 class="text-xl font-bold mb-4">{{ title }}</h4>
      <p class="text-secondary mb-6">{{ description }}</p>
      <a
        :href="link"
        class="text-primary hover:text-red-700 font-semibold inline-flex items-center"
      >
        Scopri di più <span class="ml-2">→</span>
      </a>
    </div>
  </div>
</template>

<script setup>
defineProps({
  image: {
    type: String,
    required: true
  },
  imageAlt: {
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
  link: {
    type: String,
    default: '#'
  }
});
</script>
