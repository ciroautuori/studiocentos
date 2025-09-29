<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div class="mb-4">
      <label for="name" class="block text-gray-700 text-sm font-bold mb-2">Project Name: *</label>
      <input type="text" id="name" v-model="projectData.name" required
        class="shadow border rounded w-full py-2 px-3 text-gray-700 focus:ring-2 focus:ring-blue-500" />
    </div>

    <div class="mb-4">
      <label for="description" class="block text-gray-700 text-sm font-bold mb-2">Description:</label>
      <textarea id="description" v-model="projectData.description" rows="4"
        class="shadow border rounded w-full py-2 px-3 text-gray-700 focus:ring-2 focus:ring-blue-500"></textarea>
    </div>

    <div class="mb-4">
      <label for="image" class="block text-gray-700 text-sm font-bold mb-2">Project Image:</label>
      <div class="flex flex-col space-y-2">
        <div v-if="isEditing && projectData.thumbnail_url && !imagePreview" class="mb-2">
          <p class="text-sm text-gray-600 mb-1">Current image:</p>
          <ProjectImage :image-url="projectData.thumbnail_url" :alt-text="projectData.name" size="150x150" />
        </div>

        <div v-if="imagePreview" class="mb-2">
          <p class="text-sm text-gray-600 mb-1">Image preview:</p>
          <div class="relative w-full max-w-xs">
            <img :src="imagePreview" alt="Image preview" class="h-40 object-cover rounded border border-gray-300" />
            <button @click="clearImageSelection" type="button"
              class="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 hover:bg-red-700 transition">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div class="flex flex-col">
          <input type="file" id="image" @change="handleFileUpload" accept="image/*"
            class="w-full text-gray-700 border rounded py-2 px-3 focus:ring-2 focus:ring-blue-500" />
          <p class="text-xs text-gray-500 mt-1">Supported formats: JPG, PNG, GIF (max 5MB)</p>
        </div>
      </div>
    </div>

    <div class="mb-4">
      <label for="status" class="block text-gray-700 text-sm font-bold mb-2">Status:</label>
      <select id="status" v-model="projectData.status"
        class="shadow border rounded w-full py-2 px-3 text-gray-700 focus:ring-2 focus:ring-blue-500">
        <option value="">Select status</option>
        <option value="planned">Planned</option>
        <option value="in_progress">In Progress</option>
        <option value="completed">Completed</option>
      </select>
    </div>

    <div class="mb-6">
      <label class="flex items-center">
        <input type="checkbox" v-model="projectData.is_active" class="form-checkbox h-5 w-5 text-blue-600">
        <span class="ml-2 text-gray-700">Project is active</span>
      </label>
    </div>

    <div class="flex items-center justify-between">
      <BaseButton
        type="submit"
        :disabled="isSubmitting"
        variant="primary"
      >
        {{ isSubmitting ? 'Saving...' : (isEditing ? 'Update Project' : 'Create Project') }}
      </BaseButton>
      <router-link :to="{ name: 'projects-list' }" class="text-blue-500 hover:underline font-bold text-sm">
        Cancel
      </router-link>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ApiService from '../../../services/ApiService';
import ProjectImage from '../../ui/images/ProjectImage.vue';
import BaseButton from '../../common/BaseButton.vue';

const props = defineProps({
  isEditing: {
    type: Boolean,
    default: false
  },
  projectId: {
    type: Number,
    default: null
  }
});

const emit = defineEmits(['success', 'error']);

const router = useRouter();
const isSubmitting = ref(false);
const file = ref(null);
const imagePreview = ref(null);

const projectData = reactive({
  name: '',
  description: '',
  thumbnail_url: null,
  status: '',
  is_active: true
});

const handleFileUpload = (event) => {
  const selectedFile = event.target.files[0];
  if (selectedFile) {
    if (selectedFile.size > 5 * 1024 * 1024) {
      emit('error', 'Image size exceeds 5MB limit. Please select a smaller image.');
      event.target.value = '';
      return;
    }

    file.value = selectedFile;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target.result;
    };
    reader.readAsDataURL(selectedFile);
  }
};

const clearImageSelection = () => {
  file.value = null;
  imagePreview.value = null;
  const fileInput = document.getElementById('image');
  if (fileInput) fileInput.value = '';
};

const fetchProjectData = async () => {
  if (!props.isEditing || !props.projectId) return;

  try {
    const response = await ApiService.getProject(props.projectId);
    const data = response.data;
    Object.assign(projectData, {
      name: data.name,
      description: data.description || '',
      thumbnail_url: data.thumbnail_url || null,
      status: data.status || '',
      is_active: data.is_active
    });
  } catch (err) {
    console.error("Failed to fetch project:", err);
    if (err.response?.status === 404) {
      emit('error', 'Project not found. Please return to the projects list and try again.');
    } else {
      emit('error', err.response?.data?.detail || 'Failed to load project data.');
    }
  }
};

const handleSubmit = async () => {
  if (!projectData.name.trim()) {
    emit('error', 'Project name is required.');
    return;
  }

  isSubmitting.value = true;

  try {
    const formData = new FormData();
    formData.append('name', projectData.name.trim());
    if (projectData.description) formData.append('description', projectData.description.trim());
    if (projectData.status) formData.append('status', projectData.status);
    formData.append('is_active', projectData.is_active ? 'true' : 'false');

    // Handle image upload
    if (file.value) {
      formData.append('thumbnail', file.value);
    } else if (props.isEditing && !imagePreview.value) {
      // If editing and no new image selected, keep the existing image
      formData.append('thumbnail_url', projectData.thumbnail_url || '');
    }

    let response;
    if (props.isEditing) {
      response = await ApiService.updateProject(props.projectId, formData);
    } else {
      response = await ApiService.createProject(formData);
    }

    emit('success', response.data);
    router.push({ name: 'projects-list' });
  } catch (err) {
    console.error("Error saving project:", err);
    if (err.response?.data) {
      // Handle validation errors
      const errors = err.response.data;
      if (typeof errors === 'object') {
        const errorMessages = Object.entries(errors)
          .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          .join('\n');
        emit('error', errorMessages);
      } else {
        emit('error', errors.detail || 'Error saving project.');
      }
    } else {
      emit('error', 'Error saving project. Please try again.');
    }
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(fetchProjectData);
</script>
