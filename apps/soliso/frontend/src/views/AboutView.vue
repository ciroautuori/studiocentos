<template>
  <div>
    <NavBar />
    <div class="min-h-screen">
      <!-- Hero Section -->
      <div class="relative bg-[#0b2a63] overflow-hidden">
        <!-- Background Image -->
        <div class="absolute inset-0">
          <img src="@/assets/img/hero.jpg" alt="Hero Background" class="w-full h-full object-cover opacity-20" />
        </div>
        <!-- Decorative elements -->
        <div class="absolute top-0 left-0 w-1/3 h-full bg-red-600/10 skew-x-12 transform origin-top-left"></div>
        <div class="absolute bottom-0 right-0 w-96 h-96 rounded-full bg-red-600/10 blur-3xl"></div>
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full bg-red-600/5 blur-3xl"></div>

        <div class="container mx-auto px-4 lg:px-8 relative">
          <div class="max-w-4xl mx-auto py-24">
            <div class="text-center mb-12">
              <h1 class="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
                Abbattiamo le <span class="text-red-600">Barriere</span><br>
                Costruiamo <span class="text-red-600">Inclusione</span>
              </h1>
              <p class="text-xl text-gray-200 mb-8 leading-relaxed">
                SOL.I.SO è un'associazione di promozione sociale che opera per l'inclusione
                delle persone sorde attraverso educazione, cultura e sensibilizzazione.
                Insieme per una società senza barriere.
              </p>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
              <div class="text-center">
                <div class="text-4xl font-bold text-red-600 mb-2">10+</div>
                <div class="text-gray-200">Anni di Attività</div>
              </div>
              <div class="text-center">
                <div class="text-4xl font-bold text-red-600 mb-2">1000+</div>
                <div class="text-gray-200">Persone Coinvolte</div>
              </div>
              <div class="text-center">
                <div class="text-4xl font-bold text-red-600 mb-2">50+</div>
                <div class="text-gray-200">Eventi Realizzati</div>
              </div>
              <div class="text-center">
                <div class="text-4xl font-bold text-red-600 mb-2">100%</div>
                <div class="text-gray-200">Impegno Sociale</div>
              </div>
            </div>

            <!-- CTA Buttons -->
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="/events"
                class="inline-flex items-center justify-center px-8 py-3 border border-gray-300 text-base font-medium rounded-md text-white bg-white/10 hover:bg-white/20 transition-colors duration-200"
              >
                I Nostri Eventi
                <svg class="ml-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Mission Section -->
      <div class="py-16">
        <div class="container mx-auto px-4 lg:px-8">
          <div class="grid md:grid-cols-2 gap-12 items-center">
            <div class="space-y-6">
              <h2 class="text-3xl font-bold text-gray-900">La Nostra Missione</h2>
              <p class="text-gray-600">
                Promuoviamo l'inclusione sociale delle persone sorde attraverso attività
                educative, culturali e di sensibilizzazione, contribuendo a creare una
                società più accessibile e inclusiva.
              </p>
              <ul class="space-y-4">
                <li class="flex items-start">
                  <svg class="h-6 w-6 text-red-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span class="text-gray-600">Educazione e formazione</span>
                </li>
                <li class="flex items-start">
                  <svg class="h-6 w-6 text-red-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span class="text-gray-600">Cultura e sensibilizzazione</span>
                </li>
                <li class="flex items-start">
                  <svg class="h-6 w-6 text-red-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span class="text-gray-600">Inclusione sociale</span>
                </li>
              </ul>
            </div>
            <div class="relative">
              <img
                src="/src/assets/img/about-mission.jpg"
                alt="Missione SOL.I.SO"
                class="rounded-lg shadow-xl"
              />
              <div class="absolute -bottom-6 -right-6 w-32 h-32 bg-red-600/10 rounded-full blur-2xl"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Values Section -->
      <div class="bg-[#0b2a63]/5 py-16">
        <div class="container mx-auto px-4 lg:px-8">
          <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">I Nostri Valori</h2>
          <div class="grid md:grid-cols-3 gap-8">
            <div class="bg-white p-6 rounded-lg shadow-lg">
              <div class="w-12 h-12 bg-red-600/10 rounded-lg flex items-center justify-center mb-4">
                <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">Inclusione</h3>
              <p class="text-gray-600">
                Lavoriamo per creare una società dove tutti possano partecipare attivamente,
                indipendentemente dalle differenze.
              </p>
            </div>
            <div class="bg-white p-6 rounded-lg shadow-lg">
              <div class="w-12 h-12 bg-red-600/10 rounded-lg flex items-center justify-center mb-4">
                <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">Sensibilizzazione</h3>
              <p class="text-gray-600">
                Promuoviamo la conoscenza e la comprensione della cultura sorda nella società.
              </p>
            </div>
            <div class="bg-white p-6 rounded-lg shadow-lg">
              <div class="w-12 h-12 bg-red-600/10 rounded-lg flex items-center justify-center mb-4">
                <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">Collaborazione</h3>
              <p class="text-gray-600">
                Costruiamo reti di supporto e collaborazione per raggiungere obiettivi comuni.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- History Section -->
      <div class="py-16">
        <div class="container mx-auto px-4 lg:px-8">
          <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">La Nostra Storia</h2>
            <div class="space-y-8">
              <div class="flex items-start">
                <div class="flex-shrink-0 w-12 h-12 bg-red-600/10 rounded-full flex items-center justify-center">
                  <span class="text-red-600 font-semibold">2010</span>
                </div>
                <div class="ml-6">
                  <h3 class="text-xl font-semibold text-gray-900 mb-2">Fondazione</h3>
                  <p class="text-gray-600">
                    Nasce SOL.I.SO con l'obiettivo di promuovere l'inclusione sociale delle persone sorde.
                  </p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="flex-shrink-0 w-12 h-12 bg-red-600/10 rounded-full flex items-center justify-center">
                  <span class="text-red-600 font-semibold">2015</span>
                </div>
                <div class="ml-6">
                  <h3 class="text-xl font-semibold text-gray-900 mb-2">Espansione</h3>
                  <p class="text-gray-600">
                    Ampliamo le nostre attività con nuovi progetti educativi e culturali.
                  </p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="flex-shrink-0 w-12 h-12 bg-red-600/10 rounded-full flex items-center justify-center">
                  <span class="text-red-600 font-semibold">2020</span>
                </div>
                <div class="ml-6">
                  <h3 class="text-xl font-semibold text-gray-900 mb-2">Innovazione</h3>
                  <p class="text-gray-600">
                    Introduciamo nuove metodologie e strumenti per l'inclusione sociale.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <SiteFooter />
  </div>
</template>

<script setup>
import NavBar from '@/components/layout/NavBar.vue'
import SiteFooter from '@/components/layout/SiteFooter.vue'
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
