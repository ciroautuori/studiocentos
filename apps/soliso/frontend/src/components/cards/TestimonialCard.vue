<template>
  <div class="bg-white rounded-2xl shadow-custom hover:shadow-xl transition p-8">
    <p class="text-secondary mb-6">{{ text }}</p>
    <div class="flex items-center">
      <img
        :src="avatar"
        :alt="`Avatar ${name}`"
        class="w-12 h-12 rounded-full mr-4"
      />
      <div>
        <h5 class="font-bold">{{ name }}</h5>
        <p class="text-gray-500">{{ role }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    required: true
  },
  name: {
    type: String,
    required: true
  },
  role: {
    type: String,
    required: true
  },
  avatar: {
    type: String,
    required: true
  }
});
</script>
