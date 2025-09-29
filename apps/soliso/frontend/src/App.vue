<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <RouterView />
  </div>
</template>

<style>
:root {
  --red: #c9000a;
  --blue: #005490;
  --orange: #ff6b00;
}

html {
  scroll-behavior: smooth;
}

body {
  min-height: 100vh;
  font-family: 'Inter', system-ui, sans-serif;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #1f2937;
  background-color: #f8fafc;
}

.app-container {
  min-height: 100vh;
}

/* Utility classes */
.container-custom {
  max-width: 1280px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

/* Basic button styles */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  font-weight: 500;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.btn-red {
  background-color: var(--red);
  color: white;
}

.btn-red:hover {
  background-color: #a70008;
}

.btn-blue {
  background-color: var(--blue);
  color: white;
}

.btn-blue:hover {
  background-color: #004677;
}

.btn-outline {
  background-color: transparent;
  border: 1px solid var(--red);
  color: var(--red);
}

.btn-outline:hover {
  background-color: var(--red);
  color: white;
}

/* Simple card */
.card {
  background-color: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Section helpers */
.section {
  padding-top: 3rem;
  padding-bottom: 3rem;
}

@media (min-width: 768px) {
  .section {
    padding-top: 5rem;
    padding-bottom: 5rem;
  }
}

/* Basic form styles */
input, select, textarea {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--red);
  box-shadow: 0 0 0 3px rgba(201, 0, 10, 0.2);
}
</style>

