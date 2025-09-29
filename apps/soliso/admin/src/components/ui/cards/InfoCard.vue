<template>
  <div class="bg-gray-50 p-3 sm:p-4 rounded-lg">
    <h2 class="text-lg font-semibold mb-3 sm:mb-4">{{ title }}</h2>
    <slot></slot>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  }
});
</script>
