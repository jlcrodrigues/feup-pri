<script setup lang="ts">

import Degree from '@/model/types'
import type { PropType } from 'vue';
import { useRouter } from 'vue-router';

let props = defineProps({
  degree: {
    type: Object as PropType<Degree>,
    required: true
  }
})

const descriptionMax = 200

const router = useRouter()
const openPage = () => {
  router.push({ name: 'degree', params: { id: props.degree.id } })
}

</script>

<template>
  <v-card link class="tw-m-2" @click="openPage">
    <v-card-title style="padding-bottom: 0 !important;">
        <h3 class="tw-text-xl tw-font-bold tw-text-secondary">{{ degree.name }}</h3>
    </v-card-title>
    <v-card-subtitle>
    {{ degree.duration }}
    </v-card-subtitle>
    <v-card-text>
      <p v-if="degree.description.length < descriptionMax">{{ degree.description }}</p>
      <p v-else>{{ degree.description.substring(0, descriptionMax) + "..." }}</p>
    </v-card-text>
  </v-card>
</template>
