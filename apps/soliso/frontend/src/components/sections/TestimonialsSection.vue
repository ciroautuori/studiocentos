<template>
  <section id="testimonianze" class="py-24 relative overflow-hidden bg-[#0b2a63]/5">
    <!-- Elementi decorativi di sfondo -->
    <div class="absolute top-0 left-0 w-1/3 h-full bg-[#0b2a63]/10 skew-x-12 transform origin-top-left"></div>
    <div class="absolute bottom-0 right-0 w-96 h-96 rounded-full bg-red-600/10 blur-3xl"></div>

    <div class="container mx-auto px-4 relative z-10">
      <SectionHeader
        title="Testimonianze"
        subtitle="Leggi le storie di chi ha vissuto in prima persona l'importanza dell'inclusione."
        label="Testimonianze"
        titlePrefix="Cosa dicono di "
        titleSuffix="Noi"
      />

      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <TestimonialCard
          v-for="(testimonial, index) in testimonials"
          :key="index"
          :text="testimonial.text"
          :name="testimonial.name"
          :role="testimonial.role"
          :avatar="testimonial.avatar"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import SectionHeader from '../ui/SectionHeader.vue';
import TestimonialCard from '../cards/TestimonialCard.vue';
import testimonial1m from '@/assets/img/testimonial/1m.jpg';
import testimonial1f from '@/assets/img/testimonial/1f.jpg';
import testimonial2m from '@/assets/img/testimonial/2m.jpg';
import testimonial2f from '@/assets/img/testimonial/2f.jpg';
import testimonial3m from '@/assets/img/testimonial/3m.jpg';
import testimonial3f from '@/assets/img/testimonial/3f.jpg';

const testimonials = ref([
  {
    text: '"SOL.I.SO mi ha aiutato a superare le barriere sociali che avevo sempre percepito. Grazie ai loro programmi di supporto, ora mi sento parte di una comunità che mi accetta per quello che sono."',
    name: 'Giovanni Ferretti',
    role: 'Beneficiario',
    avatar: testimonial2m
  },
  {
    text: '"Dopo anni di difficoltà nell\'inserimento lavorativo, SOL.I.SO mi ha fornito gli strumenti e la formazione necessari per trovare un impiego che valorizza le mie capacità."',
    name: 'Elena Martini',
    role: 'Utente',
    avatar: testimonial1f
  },
  {
    text: '"Come genitore di un bambino con disabilità, ho trovato in SOL.I.SO non solo supporto pratico ma anche una rete di persone che comprendono le nostre sfide quotidiane."',
    name: 'Francesco Lombardi',
    role: 'Genitore',
    avatar: testimonial1m
  },
  {
    text: '"Volontaria da tre anni, posso testimoniare l\'impatto concreto che SOL.I.SO ha sulle persone. Vedere i progressi dei partecipanti ai nostri programmi mi riempie di orgoglio."',
    name: 'Chiara Esposito',
    role: 'Volontaria',
    avatar: testimonial2f
  },
  {
    text: '"La forza di SOL.I.SO sta nella capacità di creare connessioni autentiche tra persone diverse. Attraverso i loro eventi comunitari, ho scoperto il valore della diversità."',
    name: 'Marco Ricci',
    role: 'Partecipante',
    avatar: testimonial3m
  },
  {
    text: '"Come educatrice, collaborare con SOL.I.SO ha ampliato la mia visione dell\'inclusione. I loro approcci innovativi mi hanno insegnato tecniche che ora applico quotidianamente."',
    name: 'Daniela Moretti',
    role: 'Educatrice professionale',
    avatar: testimonial3f
  }
]);
</script>
