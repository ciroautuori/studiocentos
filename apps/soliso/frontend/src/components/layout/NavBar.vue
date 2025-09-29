<template>
  <header
    class="fixed w-full bg-white/95 backdrop-blur-sm z-50 transition-all duration-300"
    :class="{ 'shadow-lg': scrolled }"
  >
    <div class="container mx-auto px-4 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center">
            <img src="/src/assets/img/logo.png" alt="Logo SOL.I.SO" class="h-10" />
          </router-link>
        </div>

        <!-- Text Size Controller - posizionato al centro in desktop -->
        <div class="hidden lg:block absolute left-1/2 transform -translate-x-1/2">
          <TextSizeController class="shadow-sm" />
        </div>

        <!-- Desktop menu -->
        <nav class="hidden lg:flex items-center space-x-2">
          <router-link
            to="/"
            class="px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 hover:bg-gray-50"
            :class="$route.path === '/' ? 'text-red-600 bg-red-50 font-semibold' : 'text-gray-700'"
            exact-active-class="text-red-600 bg-red-50 font-semibold"
          >
            Home
          </router-link>

          <router-link
            to="/about"
            class="px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 hover:bg-gray-50"
            :class="$route.path === '/about' ? 'text-red-600 bg-red-50 font-semibold' : 'text-gray-700'"
            active-class="text-red-600 bg-red-50 font-semibold"
          >
            Chi Siamo
          </router-link>

          <router-link
            to="/projects"
            class="px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 hover:bg-gray-50"
            :class="$route.path.includes('/projects') ? 'text-red-600 bg-red-50 font-semibold' : 'text-gray-700'"
            active-class="text-red-600 bg-red-50 font-semibold"
          >
            Progetti
          </router-link>

          <router-link
            to="/events"
            class="px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 hover:bg-gray-50"
            :class="$route.path.includes('/events') ? 'text-red-600 bg-red-50 font-semibold' : 'text-gray-700'"
            active-class="text-red-600 bg-red-50 font-semibold"
          >
            Eventi
          </router-link>
        </nav>

        <!-- Mobile menu button -->
        <button
          class="lg:hidden text-gray-700 hover:text-red-600 p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all duration-200"
          @click="toggleMenu"
          :aria-expanded="isMenuOpen.toString()"
          aria-label="Menu"
        >
          <svg v-if="!isMenuOpen" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile menu (slide-down animation) -->
    <div
      class="lg:hidden overflow-hidden transition-all duration-300 bg-white"
      :class="isMenuOpen ? 'max-h-screen shadow-lg border-t border-gray-100' : 'max-h-0'"
    >
      <div class="container mx-auto px-4 py-3">
        <!-- Text Size Controller in mobile -->
        <div class="mb-4 flex justify-center">
          <TextSizeController class="shadow-sm" />
        </div>

        <!-- Navigation items -->
        <nav class="flex flex-col space-y-2">
          <router-link
            to="/"
            class="px-4 py-3 rounded-md text-sm font-medium transition-all duration-200 hover:bg-gray-50"
            :class="$route.path === '/' ? 'text-red-600 bg-red-50 font-semibold' : 'text-gray-700'"
            exact-active-class="text-red-600 bg-red-50 font-semibold"
            @click="closeMenu"
          >
            Home
          </router-link>

          <router-link
            to="/about"
            class="px-4 py-3 rounded-md text-sm font-medium transition-all duration-200 hover:bg-gray-50"
            :class="$route.path === '/about' ? 'text-red-600 bg-red-50 font-semibold' : 'text-gray-700'"
            active-class="text-red-600 bg-red-50 font-semibold"
            @click="closeMenu"
          >
            Chi Siamo
          </router-link>

          <router-link
            to="/projects"
            class="px-4 py-3 rounded-md text-sm font-medium transition-all duration-200 hover:bg-gray-50"
            :class="$route.path.includes('/projects') ? 'text-red-600 bg-red-50 font-semibold' : 'text-gray-700'"
            active-class="text-red-600 bg-red-50 font-semibold"
            @click="closeMenu"
          >
            Progetti
          </router-link>

          <router-link
            to="/events"
            class="px-4 py-3 rounded-md text-sm font-medium transition-all duration-200 hover:bg-gray-50"
            :class="$route.path.includes('/events') ? 'text-red-600 bg-red-50 font-semibold' : 'text-gray-700'"
            active-class="text-red-600 bg-red-50 font-semibold"
            @click="closeMenu"
          >
            Eventi
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import TextSizeController from '../ui/TextSizeController.vue';

const $route = useRoute();
const isMenuOpen = ref(false);
const scrolled = ref(false);
const currentHash = ref('');

// Toggle mobile menu
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
  if (isMenuOpen.value) {
    document.body.classList.add('overflow-hidden');
  } else {
    document.body.classList.remove('overflow-hidden');
  }
};

// Close mobile menu
const closeMenu = () => {
  if (isMenuOpen.value) {
    isMenuOpen.value = false;
    document.body.classList.remove('overflow-hidden');
  }
};

// Check if a specific hash is active
const isHashActive = (hash) => {
  return currentHash.value === hash;
};

// Improved scroll to section function with offset and smooth behavior
const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId);
  if (element) {
    const headerOffset = 80; // Adjust based on your header height
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });

    // Update hash without triggering scroll
    currentHash.value = sectionId;
    history.pushState(null, null, `#${sectionId}`);
  }
};

// Scroll to section and close mobile menu
const scrollToSectionAndCloseMenu = (sectionId) => {
  closeMenu();
  setTimeout(() => {
    scrollToSection(sectionId);
  }, 300);
};

// Handle scroll events with improved section detection
const handleScroll = () => {
  scrolled.value = window.scrollY > 20;
  checkVisibleSections();
};

// Improved section visibility check with intersection observer
const checkVisibleSections = () => {
  const sections = ['contatti'];
  const headerOffset = 80;

  for (const section of sections) {
    const element = document.getElementById(section);
    if (element) {
      const rect = element.getBoundingClientRect();
      const elementTop = rect.top + window.pageYOffset;
      const elementBottom = elementTop + rect.height;
      const scrollPosition = window.pageYOffset + headerOffset;

      if (scrollPosition >= elementTop && scrollPosition < elementBottom) {
        currentHash.value = section;
        break;
      }
    }
  }
};

// Watch for route changes
watch(() => $route.path, (newPath) => {
  closeMenu();

  // Se siamo in una pagina di progetto o eventi, aggiorna il link attivo
  if (newPath.startsWith('/projects') || newPath.startsWith('/events')) {
    currentHash.value = '';
  }
});

// Watch for hash changes
watch(() => window.location.hash, (newHash) => {
  if (newHash) {
    const sectionId = newHash.substring(1);
    if (['contatti'].includes(sectionId)) {
      currentHash.value = sectionId;
      scrollToSection(sectionId);
    }
  } else {
    // Se non c'è hash e siamo in una pagina di progetto o eventi, mantieni il link attivo
    if ($route.path.startsWith('/projects') || $route.path.startsWith('/events')) {
      currentHash.value = '';
    }
  }
});

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 1024 && isMenuOpen.value) {
      closeMenu();
    }
  });

  // Initialize scroll state
  handleScroll();

  // Handle initial hash
  if (window.location.hash) {
    const sectionId = window.location.hash.substring(1);
    if (['contatti'].includes(sectionId)) {
      currentHash.value = sectionId;
      setTimeout(() => scrollToSection(sectionId), 100);
    }
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  window.removeEventListener('resize', () => {});
  document.body.classList.remove('overflow-hidden');
});
</script>
