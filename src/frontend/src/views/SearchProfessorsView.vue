
<script setup lang="ts">
import { ref } from 'vue'
import { Professor } from '@/model/types';
import SearchBar from '@/components/SearchBar.vue';
import ProfessorCard from '@/components/ProfessorCard.vue';
import { useRoute, useRouter } from 'vue-router';
import useApiStore from '@/stores/api';

const route = useRoute()
const search = ref(route.query.text as string)

const router = useRouter()

const professors = ref([] as Professor[])

const apiStore = useApiStore()
const getSearch = async () => {
  professors.value = await apiStore.searchProfessors(search.value)
}

if (search.value) {
  getSearch()
}

</script>

<template>
  <div class="tw-flex tw-align-center tw-flex-col">
    <div class="tw-sticky tw-z-10 tw-top-0 tw-bg-white tw-pb-3 tw-px-5 tw-shadow">
      <div class="tw-md:w-3/4 tw-mt-5">
        <search-bar v-model="search" @input="getSearch()"></search-bar>
      </div>
      <nav class="tw-flex tw-gap-2">
        <v-chip variant="elevated" @click="router.push({ name: 'search', query: { text: search } })">{{ $t('professors') }}</v-chip>
      </nav>
    </div>
    <div class="tw-m-5">
      <professor-card v-for="professor in professors" :professor="professor"></professor-card>
    </div>
  </div>
</template>