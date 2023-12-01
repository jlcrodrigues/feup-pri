<script setup lang="ts">
import { ref } from 'vue'
import { VTextField } from 'vuetify/components';
import useApiStore from '@/stores/api'
import Course from '@/model/types'
import { useRoute } from 'vue-router';
import { watch } from 'fs';
import { onBeforeMount } from 'vue';
import { onMounted } from 'vue';

const route = useRoute()
const id = ref(route.params.id as string)

const course = ref({} as Course)

const apiStore = useApiStore()
onMounted(async () => {
  course.value = await apiStore.getCourse(id.value)
})

const contents = ['objective', 'results', 'workingMethod', 'preRequirements', 'program', 'evaluationType', 'passingRequirements']

</script>

<template>
  <v-card class="tw-m-10">
    <v-card-title>
      <div class="tw-flex tw-justify-start tw-gap- tw-items-baseline">
        <h2 class="tw-text-primary tw-text-3xl">{{ course.name }}</h2>
        <v-btn variant="text" density="compact" :href="course.url" target="_blank">
          <v-icon class="tw-text-secondary">mdi-open-in-new</v-icon>
        </v-btn>
      </div>
      <div class="tw-flex tw-text-lg tw-text-secondary-light tw-font-light tw-items-center">
        <span>{{ course.language }}</span>
        <span class="tw-ml-2 tw-text-primary-lighth tw-font-normal tw-bg-background tw-px-2.5 tw-rounded">{{ course.ects
        }} ECTS</span>
      </div>
    </v-card-title>
    <v-card-text>
      <article>
        <section v-for="content in contents" :key="content" class="tw-mt-5">
          <template v-if="course[content]">
            <h5 class="tw-text-2xl tw-text-secondary">{{ $t(content) }}</h5>
            <p>{{ course[content] }}</p>
          </template>
        </section>
      </article>
    </v-card-text>
  </v-card>
</template>
