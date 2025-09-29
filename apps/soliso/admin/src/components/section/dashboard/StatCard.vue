<template>
  <div class="bg-white overflow-hidden shadow rounded-lg transition-all duration-300 hover:shadow-lg hover:scale-[1.02]">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <div :class="`p-3 rounded-full ${iconBgColor}`">
            <component :is="icon" :class="`h-6 w-6 ${iconColor}`" />
          </div>
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">
              {{ title }}
            </dt>
            <dd class="flex items-baseline">
              <div class="text-2xl font-semibold text-gray-900">
                {{ value }}
              </div>
              <div v-if="trend" :class="`ml-2 flex items-baseline text-sm font-semibold ${trendColor}`">
                <component :is="trendIcon" class="h-4 w-4" />
                <span class="ml-1">{{ trend }}</span>
              </div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  icon: {
    type: Object,
    required: true
  },
  iconBgColor: {
    type: String,
    default: 'bg-blue-50'
  },
  iconColor: {
    type: String,
    default: 'text-blue-600'
  },
  trend: {
    type: String,
    default: null
  },
  trendIcon: {
    type: Object,
    default: null
  }
})

const trendColor = computed(() => {
  if (!props.trend) return ''
  return props.trend.startsWith('+') ? 'text-green-600' : 'text-red-600'
})
</script>
