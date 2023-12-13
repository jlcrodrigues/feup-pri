
<script setup lang="ts">
import { ref } from 'vue'
import { Degree } from '@/model/types';
import DegreeCard from '@/components/DegreeCard.vue';
import SearchFilter from '@/components/SearchFilter.vue';
import SearchBar from '@/components/SearchBar.vue';
import SearchOrder from '@/components/SearchOrder.vue';
import { useRoute, useRouter } from 'vue-router';
import useApiStore from '@/stores/api';
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';
const { t } = useI18n()

const route = useRoute()
const search = ref(route.query.text as string)

const typesOfCourse = ['Licenciatura', 'Mestrado', 'Mestrado Integrado']
const typeOfCourse = ref(route.query.typeOfCourse as Array<string>)

const keys = computed(() => ['duration'])
const key = ref(route.query.order as string)

const order = ref(route.query.order as string)
if (!order.value) order.value = 'asc'

const router = useRouter()

const degrees = ref([] as Degree[])

const apiStore = useApiStore()
const getSearch = async () => {
  degrees.value = await apiStore.searchDegrees({ text: search.value, typeOfCourse: typeOfCourse.value, sortKey: key.value, sortOrder: order.value })
  router.push({ name: 'degrees', query: { text: search.value, typeOfCourse: typeOfCourse.value, sortKey: key.value, sortOrder: order.value } })
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
        <v-chip variant="elevated" @click="router.push({ name: 'search', query: { text: search } })">{{ $t('degrees')
        }}</v-chip>
        <search-filter :name="$t('studyCycle')" :list="typesOfCourse" v-model="typeOfCourse"
          @update:model-value="getSearch()"></search-filter>
        <search-order :name="$t('sort')" :list="keys" v-model:criteria="key" v-model:order="order"
          @update="getSearch()"></search-order>
      </nav>
    </div>
    <div class="tw-m-5">
      <degree-card v-for="degree in degrees" :degree="degree"></degree-card>
    </div>
  </div>
</template>