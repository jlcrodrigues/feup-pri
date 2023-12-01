<script setup lang="ts">
import { ref } from 'vue'
import { CourseUnit, Degree, Professor } from '@/model/types';
import CourseCard from '@/components/CourseCard.vue';
import DegreeCard from '@/components/DegreeCard.vue';
import ProfessorCard from '@/components/ProfessorCard.vue';
import SearchBar from '@/components/SearchBar.vue';
import { useRoute, useRouter } from 'vue-router';
import useApiStore from '@/stores/api';
import { computed } from 'vue';

const route = useRoute()
const search = ref(route.query.text as string)

const router = useRouter()
if (!search.value) {
  router.push({ name: 'home' })
}

const degrees = ref([] as Degree[])
const courses = ref([] as CourseUnit[])
const professors = ref([] as Professor[])

const apiStore = useApiStore()
const getSearch = async () => {
  degrees.value = (await apiStore.searchDegrees(search.value)).slice(0, 3)
  courses.value = (await apiStore.searchCourses(search.value)).slice(0, 3)
  professors.value = (await apiStore.searchProfessors(search.value)).slice(0, 3)
}

if (search.value) {
  getSearch()
}

const resultsEmpty = computed(() => {
  return degrees.value.length == 0 && courses.value.length == 0 && professors.value.length == 0
})

</script>

<template>
  <div class="tw-flex tw-align-center tw-flex-col">
    <div class="tw-sticky tw-z-10 tw-top-0 tw-bg-white tw-pb-3 tw-px-5 tw-shadow">
      <div class="tw-md:w-3/4 tw-mt-5">
        <search-bar v-model="search" @input="getSearch()"></search-bar>
      </div>
      <nav class="tw-flex tw-gap-2">
        <v-chip variant="outlined" @click="router.push({ name: 'degrees', query: { text: search } })">{{ $t('degrees')
        }}</v-chip>
        <v-chip variant="outlined" @click="router.push({ name: 'courses', query: { text: search } })">{{ $t('courses')
        }}</v-chip>
        <v-chip variant="outlined" @click="router.push({ name: 'professors', query: { text: search } })">{{
          $t('professors') }}</v-chip>
      </nav>
    </div>
    <div v-if="resultsEmpty" class="tw-flex tw-text-xl tw-mt-5 tw-justify-center">
      {{ $t('noResults') }}
    </div>
    <div v-else class="tw-mx-5">
      <div v-if="degrees.length != 0" class="tw-mt-5">
        <h2 class="tw-text-xl tw-font-semibold">{{ $t('degrees') }}</h2>
        <degree-card v-for="degree in degrees" :degree="degree"></degree-card>
      </div>
      <div v-if="courses.length != 0" class="tw-mt-5">
        <h2 class="tw-text-xl tw-font-semibold">{{ $t('courses') }}</h2>
        <course-card v-for="course in courses" :course="course"></course-card>
      </div>
      <div v-if="professors.length != 0" class="tw-mt-5">
        <h2 class="tw-text-xl tw-font-semibold">{{ $t('professors') }}</h2>
        <professor-card v-for="professor in professors" :professor="professor"></professor-card>
      </div>
    </div>
  </div>
</template>
