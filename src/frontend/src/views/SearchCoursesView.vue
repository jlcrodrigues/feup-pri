
<script setup lang="ts">
import { ref } from 'vue'
import { VTextField } from 'vuetify/components';
import useApiStore from '@/stores/store'
import { CourseUnit, Degree } from '@/model/modelTypes';
import CourseCard from '@/components/CourseCard.vue';
import SearchBar from '@/components/SearchBar.vue';
import { useRoute, useRouter } from 'vue-router';
import { watch } from 'fs';

const route = useRoute()
const search = ref(route.query.text as string)

const router = useRouter()

const courses = ref([] as CourseUnit[])

const getSearch = async () => {
  getCourses()
}

const getCourses = async () => {
  const response = await fetch(`${useApiStore().url}/search/courses?text=${search.value}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/text'
    },
  })
  const results = await response.json()
  courses.value = results.results
}


if (search.value) {
  getSearch()
}


</script>

<template>
  <div class="tw-flex tw-align-center tw-flex-col tw-m-5">
    <div class="tw-md:w-3/4 tw-mt-5">
      <search-bar v-model="search" @input="getSearch()"></search-bar>
    </div>
    <nav class="tw-flex tw-gap-2">
      <v-chip variant="elevated" @click="router.push({ name: 'search', query: {text: search }})">Course Units</v-chip>
    </nav>
    <div class="tw-mt-5">
      <course-card v-for="course in courses" :course="course"></course-card>
    </div>
  </div>
</template>
