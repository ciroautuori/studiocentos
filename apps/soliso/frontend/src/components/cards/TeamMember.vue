<template>
  <div class="bg-white rounded-2xl shadow-custom hover:shadow-xl transition overflow-hidden">
    <img :src="image" :alt="`Team Member ${name}`" class="w-full h-64 object-cover" />
    <div class="p-6">
      <h4 class="text-xl font-bold">{{ name }}</h4>
      <h5 class="text-primary mb-4">{{ role }}</h5>
      <p class="text-gray-600 mb-4">{{ description }}</p>
      <div class="flex space-x-4">
        <a
          v-for="(link, index) in socialLinks"
          :key="index"
          :href="link.url"
          class="text-primary hover:text-red-700"
          target="_blank"
          rel="noopener noreferrer"
        >
          <i :class="link.icon"></i>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    required: true
  },
  role: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  image: {
    type: String,
    required: true
  },
  socialLinks: {
    type: Array,
    default: () => []
  }
});
</script>
