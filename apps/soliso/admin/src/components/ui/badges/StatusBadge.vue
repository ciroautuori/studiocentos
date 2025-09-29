<template>
  <span :class="[
    'px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-medium',
    {
      'bg-green-100 text-green-800': status === 'completed',
      'bg-yellow-100 text-yellow-800': status === 'in_progress',
      'bg-blue-100 text-blue-800': status === 'planned',
      'bg-gray-100 text-gray-800': !status
    }
  ]">
    {{ status || 'Not set' }}
  </span>
</template>

<script setup>
defineProps({
  status: {
    type: String,
    default: ''
  }
});
</script>
