<script setup lang="ts">

import { CourseUnit } from '@/model/types';
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
  router.push({ name: 'course', params: { id: props.course.id } })
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
    <v-card-text v-if="course.objectives">
      <p v-if="course.objectives.length < descriptionMax">{{ course.objectives }}</p>
      <p v-else>{{ course.objectives.substring(0, descriptionMax) + "..." }}</p>
    </v-card-text>
  </v-card>
</template>
