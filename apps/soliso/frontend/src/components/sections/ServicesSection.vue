<template>
  <section id="servizi" class="py-24 relative overflow-hidden bg-red-600/5">
    <!-- Elementi decorativi di sfondo -->
    <div class="absolute top-0 left-0 w-1/3 h-full bg-red-600/10 skew-x-12 transform origin-top-left"></div>
    <div class="absolute bottom-0 right-0 w-96 h-96 rounded-full bg-[#0b2a63]/10 blur-3xl"></div>

    <div class="container mx-auto px-4 relative z-10">
      <SectionHeader
        title="Servizi"
        subtitle="Scopri i nostri servizi studiati per facilitare la comunicazione e l'inclusione."
        label="Servizi"
        titlePrefix="I Nostri "
        titleSuffix="Servizi"
      />

      <div class="grid md:grid-cols-2 gap-8">
        <ServiceCard
          v-for="(service, index) in services"
          :key="index"
          :image="service.image"
          :image-alt="service.imageAlt"
          :title="service.title"
          :description="service.description"
          :link="service.link"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import SectionHeader from '../ui/SectionHeader.vue';
import ServiceCard from '../cards/ServiceCard.vue';
import assistenzaImage from '@/assets/img/Assistenza-specialistica.jpg';
import formazioneImage from '@/assets/img/formazione.jpg';

const services = ref([
  {
    image: assistenzaImage,
    imageAlt: 'Assistenza Specialistica per Sordi',
    title: 'Assistenza Specialistica',
    description: 'Servizio di supporto completo per persone sorde, inclusi interpreti LIS, consulenza specializzata e supporto personalizzato per una comunicazione efficace e inclusiva.',
    link: '#'
  },
  {
    image: formazioneImage,
    imageAlt: 'Formazione Accessibile per Sordi',
    title: 'Formazione Accessibile',
    description: 'Programmi di formazione inclusivi con interpreti LIS e materiali didattici adattati, per garantire pari opportunità e accesso alla conoscenza.',
    link: '#'
  }
]);
</script>
