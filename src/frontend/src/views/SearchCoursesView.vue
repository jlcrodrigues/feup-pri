
<script setup lang="ts">
import { ref } from 'vue'
import { CourseUnit, Degree } from '@/model/types';
import CourseCard from '@/components/CourseCard.vue';
import SearchBar from '@/components/SearchBar.vue';
import SearchFilter from '@/components/SearchFilter.vue';
import { useRoute, useRouter } from 'vue-router';
import useApiStore from '@/stores/api';

const route = useRoute()

const search = ref(route.query.text as string)
const languages = ['Português', 'Inglês']
const language = ref(route.query.language as Array<string>)


const router = useRouter()

const courses = ref([] as CourseUnit[])

const apiStore = useApiStore()
const getSearch = async () => {
  router.push({ name: 'courses', query: { text: search.value, language: language.value } })
  courses.value = await apiStore.searchCourses({text: search.value, language: language.value})
}

getSearch()

</script>

<template>
  <div class="tw-flex tw-align-center tw-flex-col">
    <div class="tw-sticky tw-z-10 tw-top-0 tw-bg-white tw-pb-3 tw-px-5 tw-shadow">
      <div class="tw-md:w-3/4 tw-mt-5">
        <search-bar v-model="search" @input="getSearch()"></search-bar>
      </div>
      <nav class="tw-flex tw-gap-2">
        <v-chip variant="elevated" @click="router.push({ name: 'search', query: { text: search } })">{{ $t('courses') }}</v-chip>
        <search-filter :name="$t('language')" :list="languages" v-model="language" @update:model-value="getSearch()"></search-filter>
      </nav>
    </div>
    <div class="tw-m-5">
      <course-card v-for="course in courses" :course="course"></course-card>
    </div>
  </div>
</template>
