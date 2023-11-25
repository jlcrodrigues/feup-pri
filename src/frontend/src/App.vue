<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'

import HomeView from './views/HomeView.vue'
import AppHeader from './components/app/AppHeader.vue';

</script>

<template>
  <app-header></app-header>

  <RouterView />
</template>

<style scoped></style>
