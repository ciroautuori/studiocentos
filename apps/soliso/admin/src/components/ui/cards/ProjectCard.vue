<template>
  <div class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden">
    <ProjectImage
      :image-url="project.thumbnail_url"
      :alt-text="project.title"
      class="w-full"
    />
    <div class="p-4">
      <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ project.title }}</h3>
      <p class="text-gray-600 text-sm mb-4 line-clamp-2">{{ project.description }}</p>
      <div class="flex items-center justify-between">
        <StatusBadge :status="project.status" />
        <ActiveBadge :is-active="project.is_active" />
      </div>
      <div class="mt-4 flex items-center justify-between text-sm text-gray-500">
        <span>{{ formatDate(project.created_at) }}</span>
        <BaseButton
          variant="primary"
          size="small"
          @click="$emit('view', project)"
        >
          View Details
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatDate } from '../../../utils/dateUtils';
import ProjectImage from '../images/ProjectImage.vue';
import StatusBadge from '../badges/StatusBadge.vue';
import ActiveBadge from '../badges/ActiveBadge.vue';
import BaseButton from '../../common/BaseButton.vue';

defineProps({
  project: {
    type: Object,
    required: true
  }
});

defineEmits(['view']);
</script>
