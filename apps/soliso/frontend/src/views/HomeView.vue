<template>
  <div class="min-h-screen bg-white text-gray-800 font-sans">
    <NavBar />
    <HeroSection />
    <AboutSection />
    <ProjectsSection />
    <ServicesSection />
    <EventsSection />
    <TestimonialsSection />
    <TeamSection />
    <ContactSection />
    <SiteFooter />
  </div>
</template>

<script setup>
import NavBar from '@/components/layout/NavBar.vue';
import SiteFooter from '@/components/layout/SiteFooter.vue';
import HeroSection from '@/components/sections/HeroSection.vue';
import AboutSection from '@/components/sections/AboutSection.vue';
import ProjectsSection from '@/components/sections/ProjectsSection.vue';
import ServicesSection from '@/components/sections/ServicesSection.vue';
import EventsSection from '@/components/sections/EventsSection.vue';
import TestimonialsSection from '@/components/sections/TestimonialsSection.vue';
import TeamSection from '@/components/sections/TeamSection.vue';
import ContactSection from '@/components/sections/ContactSection.vue';
</script>
