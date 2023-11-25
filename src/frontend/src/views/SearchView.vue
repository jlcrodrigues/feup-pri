<script setup lang="ts">
import { ref } from 'vue'
import { VTextField } from 'vuetify/components';
import useApiStore from '@/stores/store'
import Degree from '@/model/customTypes'
import DegreeCard from '@/components/DegreeCard.vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const search = ref(route.query.text as string)

const degrees = ref([] as Degree[])

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

if (search.value) {
  getSearch()
}
</script>

<template>
  <div class="tw-flex tw-align-center tw-flex-col">
    <div class="tw-md:w-3/4 tw-m-5">
      <v-text-field v-model="search" label="Search" @keydown.enter="getSearch">
      </v-text-field>
    </div>
    <degree-card v-for="degree in degrees" :degree="degree"></degree-card>
  </div>
</template>
