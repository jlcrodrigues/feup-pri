<script setup lang="ts">
import { ref } from 'vue'
import SearchBar from '@/components/SearchBar.vue';
import { useRouter } from 'vue-router';

let search = ref('')

const router = useRouter()

const getSearch = async () => {
  router.push({ name: 'search', query: { text: search.value } })
}
</script>

<template>
  <div class="tw-bg-background tw-flex tw-align-center tw-flex-col tw-items-center tw-justify-center tw-h-screen">
    <h1 class="tw-text-8xl tw-font-thin tw-mb-0"><span class="tw-text-secondary">Academic</span><span class="tw-text-primary">Quest</span>
    </h1>
    <h6 class="tw-text-2xl tw-mt-1 tw-font-thin tw-italic">
      {{ $t('slogan') }}
    </h6>
    <div class="md:tw-w-3/4 tw-m-5">
      <search-bar v-model="search" @keydown.enter="getSearch()"></search-bar>
    </div>
  </div>
</template>
