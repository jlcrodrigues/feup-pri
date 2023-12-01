<script setup lang="ts">

import { CourseUnit } from '@/model/modelTypes';
import type { PropType } from 'vue';
import { useRouter } from 'vue-router';

let props = defineProps({
  course: {
    type: Object as PropType<CourseUnit>,
    required: true
  }
})

const descriptionMax = 200

const router = useRouter()
const openPage = () => {
    // TODO: course page
  //router.push({ name: 'degree', query: { id: props.degree.id } })
}

</script>

<template>
  <v-card link class="tw-m-2" @click="openPage">
    <v-card-title style="padding-bottom: 0 !important;">
        <h3 class="tw-text-xl tw-font-bold tw-text-secondary">{{ course.name }}</h3>
    </v-card-title>
    <v-card-subtitle>
    {{ course.code }} - {{ course.ects }} ECTS
    </v-card-subtitle>
    <v-card-text>
      <p v-if="course.objective.length < descriptionMax">{{ course.objective }}</p>
      <p v-else>{{ course.objective.substring(0, descriptionMax) + "..." }}</p>
    </v-card-text>
  </v-card>
</template>
