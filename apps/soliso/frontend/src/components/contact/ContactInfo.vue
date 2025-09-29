<template>
  <div class="flex items-start">
    <div class="text-2xl text-primary mr-4">
      <i :class="icon"></i>
    </div>
    <div>
      <h5 class="font-bold">{{ title }}</h5>
      <p class="text-gray-600">{{ value }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  value: {
    type: String,
    required: true
  }
});
</script>
