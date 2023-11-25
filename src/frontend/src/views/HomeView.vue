<script setup lang="ts">
import { ref } from 'vue'
import { VTextField } from 'vuetify/components';
import useApiStore from '@/stores/store'
import Degree from '@/model/customTypes'
import DegreeCard from '@/components/DegreeCard.vue';

let search = ref('')

let degrees = ref([] as Degree[])

const getSearch = async () => {
  const response = await fetch(`${useApiStore().url}/search?text=${search.value}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/text'
    },
  })
  const results = await response.json()
  degrees.value = results.results
}
</script>

<template>
  <div class="flex align-center flex-col">
    <div class="md:w-3/4 m-5">
      <v-text-field v-model="search" label="Search" @keydown.enter="getSearch">
      </v-text-field>
    </div>
    <degree-card v-for="degree in degrees" :degree="degree"></degree-card>
  </div>
</template>
