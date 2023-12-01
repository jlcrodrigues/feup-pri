<script setup lang="ts">

import Professor from '@/model/types'
import type { PropType } from 'vue';
import { useRouter } from 'vue-router';

let props = defineProps({
  professor: {
    type: Object as PropType<Professor>,
    required: true
  }
})

const descriptionMax = 200

const router = useRouter()
const openPage = () => {
  // TODO: professor page
  //router.push({ name: 'professor', query: { id: props.degree.id } })
}

</script>

<template>
  <v-card link class="tw-m-2" @click="openPage">
    <v-card-title style="padding-bottom: 0 !important;">
      <h3 class="tw-text-xl tw-font-bold tw-text-secondary">{{ professor.name }}</h3>
    </v-card-title>
    <v-card-subtitle>
    </v-card-subtitle>
    <v-card-text>
      <p v-if="professor.personalPresentation.length < descriptionMax">{{ professor.personalPresentation }}</p>
      <p v-else>{{ professor.personalPresentation.substring(0, descriptionMax) + "..." }}</p>
    </v-card-text>
  </v-card>
</template>
