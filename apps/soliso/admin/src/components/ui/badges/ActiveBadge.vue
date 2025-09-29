<template>
  <span :class="[
    'px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-medium',
    {
      'bg-green-100 text-green-800': isActive,
      'bg-red-100 text-red-800': !isActive
    }
  ]">
    {{ isActive ? 'Active' : 'Inactive' }}
  </span>
</template>

<script setup>
defineProps({
  isActive: {
    type: Boolean,
    default: false
  }
});
</script>
