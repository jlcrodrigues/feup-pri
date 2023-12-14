
<script setup lang="ts">
import { ref } from 'vue'
import { Professor } from '@/model/types';
import SearchBar from '@/components/SearchBar.vue';
import SearchFilter from '@/components/SearchFilter.vue';
import SearchOrder from '@/components/SearchOrder.vue';
import ProfessorCard from '@/components/ProfessorCard.vue';
import { useRoute, useRouter } from 'vue-router';
import useApiStore from '@/stores/api';

const route = useRoute()
const search = ref(route.query.text as string)

const statuses=['Ativo', 'Não Ativo']
const status = ref(route.query.status as Array<string>)

const ranks = ['Professor Catedrático', 'Professor Associado', 'Professor Associado Convidado', 'Professor Auxiliar', 'Professor Auxiliar Convidado', 'Assistente', 'Assistente Convidado']
const rank = ref(route.query.rank as Array<string>)

const keys = ['name']
const key = ref(route.query.order as string)

const order = ref(route.query.order as string)
if (!order.value) order.value = 'asc'

const router = useRouter()

const professors = ref([] as Professor[])

const apiStore = useApiStore()
const getSearch = async () => {
  professors.value = await apiStore.searchProfessors({text: search.value, status: status.value, rank: rank.value, sortKey: key.value, sortOrder: order.value})
  router.push({ name: 'professors', query: { text: search.value, status: status.value, rank: rank.value, sortKey: key.value, sortOrder: order.value } })
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
        <v-chip variant="elevated" @click="router.push({ name: 'search', query: { text: search } })">{{ $t('professors') }}</v-chip>
        <search-filter :name="$t('status')" :list="statuses" v-model="status" @update:model-value="getSearch()"></search-filter>
        <search-filter :name="$t('rank')" :list="ranks" v-model="rank" @update:model-value="getSearch()"></search-filter>
        <search-order :name="$t('sort')" :list="keys" v-model:criteria="key" v-model:order="order"
          @update="getSearch()"></search-order>
      </nav>
    </div>
    <div class="tw-m-5">
      <professor-card v-for="professor in professors" :professor="professor"></professor-card>
    </div>
  </div>
</template>