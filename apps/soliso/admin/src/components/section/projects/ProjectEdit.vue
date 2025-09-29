<template>
  <div class="bg-white rounded-lg shadow">
    <div class="border-b border-gray-200 bg-gray-50 px-4 py-5 sm:px-6">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <h3 class="text-lg font-medium leading-6 text-gray-900">Edit Project</h3>
        <div class="mt-4 flex flex-col sm:mt-0 sm:flex-row sm:space-x-3 space-y-3 sm:space-y-0">
          <router-link :to="{ name: 'projects-list' }"
            class="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-150">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Projects
          </router-link>
        </div>
      </div>
    </div>

    <div class="p-6">
      <div v-if="loading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
        <p class="mt-2 text-gray-600">Loading project details...</p>
      </div>

      <div v-if="error" class="rounded-md bg-red-50 p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">{{ error }}</h3>
          </div>
        </div>
      </div>

      <div v-if="!isValidId" class="rounded-md bg-red-50 p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Invalid project ID. Please return to the projects list and try again.</h3>
          </div>
        </div>
      </div>

      <div v-if="!loading && isValidId" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-6">
            <div class="bg-white shadow rounded-lg overflow-hidden">
              <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 class="text-lg font-medium leading-6 text-gray-900">Basic Information</h3>
              </div>
              <div class="px-4 py-5 sm:p-6">
                <ProjectForm
                  :is-editing="true"
                  :project-id="projectId"
                  @success="handleSuccess"
                  @error="handleError"
                />
              </div>
            </div>
          </div>

          <div class="bg-white shadow rounded-lg overflow-hidden">
            <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 class="text-lg font-medium leading-6 text-gray-900">Project Image</h3>
            </div>
            <div class="px-4 py-5 sm:p-6">
              <div class="text-gray-500 text-sm">
                Image preview will be shown here
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import PageHeader from '../../../components/ui/headers/PageHeader.vue';
import ProjectForm from '../../../components/section/projects/ProjectForm.vue';

const route = useRoute();
const router = useRouter();
const loading = ref(false);
const error = ref(null);

const projectId = computed(() => {
  const id = parseInt(route.params.id);
  return isNaN(id) ? null : id;
});

const isValidId = computed(() => projectId.value !== null);

const pageTitle = computed(() => 'Edit Project');

const handleSuccess = (data) => {
  console.log('Project updated successfully:', data);
  router.push({ name: 'projects-list' });
};

const handleError = (message) => {
  error.value = message;
};
</script>
