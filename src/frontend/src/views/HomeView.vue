<script setup lang="ts">
import { ref } from 'vue'
import { VTextField } from 'vuetify/components';
import useApiStore from '@/stores/store'
import Degree from '@/model/customTypes'
import DegreeCard from '@/components/DegreeCard.vue';
import { useRouter } from 'vue-router';

let search = ref('')

const router = useRouter()

const getSearch = async () => {
  router.push({ name: 'search', query: { text: search.value } })
}
</script>

<template>
  <div class="tw-flex tw-align-center tw-flex-col tw-items-center tw-justify-center tw-h-screen">
    <h1 class="tw-text-7xl tw-font-medium"><span class="tw-text-secondary">Academic</span><span class="tw-text-primary">Quest</span>
    </h1>
    <div class="md:tw-w-3/4 tw-m-5">
      <v-text-field v-model="search" label="Search" @keydown.enter="getSearch">
      </v-text-field>
    </div>
  </div>
</template>
