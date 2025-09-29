<template>
  <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 sm:gap-4 mb-4 sm:mb-6">
    <h1 class="text-xl sm:text-2xl font-semibold">{{ title }}</h1>
    <div class="flex flex-col sm:flex-row gap-2 w-full sm:w-auto">
      <slot name="actions"></slot>
    </div>
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
