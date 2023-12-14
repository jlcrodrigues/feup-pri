<script setup lang="ts">
import { ref, watch } from 'vue'
import { VTextField } from 'vuetify/components';
import useApiStore from '@/stores/api'
import Degree from '@/model/types'
import { useRoute, useRouter } from 'vue-router';
import { onBeforeMount } from 'vue';
import { onMounted } from 'vue';

const route = useRoute()
const router = useRouter()
const id = ref(route.params.id as string)

const degree = ref({} as Degree)
degree.value.courses = []

const related = ref([] as Degree[])

const apiStore = useApiStore()
const getDegree = async () => {
  degree.value = await apiStore.getDegree(id.value)
  getRelated()
}

const getRelated = async () => {
  related.value = await apiStore.getRelatedDegrees(id.value)
}

watch(() => route.params.id, () => {
  router.go(0)
})

onMounted(() => {
  getDegree()
})

const descriptionMax = 150

let page = ref(1);
const coursesPerPage = 6;

</script>

<template>
  <v-card class="tw-m-10">
    <v-card-title>
      <div class="tw-flex tw-justify-start tw-gap- tw-items-baseline">
        <h2 class="tw-text-primary tw-text-3xl">{{ degree.name }}</h2>
        <v-btn v-if="degree.url" variant="text" density="compact" :href="degree.url" target="_blank">
          <v-icon class="tw-text-secondary">mdi-open-in-new</v-icon>
        </v-btn>
      </div>
      <div class="tw-flex tw-text-lg tw-text-secondary-light tw-font-light tw-items-center">
        <span>{{ degree.duration }}</span>
        <span class="tw-ml-2 tw-text-primary-lighth tw-font-normal tw-bg-background tw-px-2.5 tw-rounded">{{
          degree.type_of_course }}</span>
      </div>
    </v-card-title>
    <v-card-text>
      <article>
        <section class="tw-mb-5">
          {{ degree.description }}
        </section>

        <section v-if="degree.outings" class="tw-mb-5">
          <h5 class="tw-text-2xl tw-text-secondary">{{ $t('outings') }}</h5>
          <p>{{ degree.outings }}</p>
        </section>

        <!-- Courses -->
        <section>
          <h5 class="tw-text-2xl tw-text-center tw-text-secondary">{{ $t('courses') }}</h5>
          <div class="tw-flex tw-flex-wrap tw-justify-center" style="min-height: 450px;">
            <div v-for="course in degree.courses.slice((page - 1) * coursesPerPage, page * coursesPerPage)"
              :key="course.id" class="tw-border tw-rounded tw-m-2 tw-p-2" style="width: 300px;">
              <router-link :to="{ name: 'course', params: { id: course.id } }">
                <p class="tw-text-xl tw-text-primary tw-whitespace-pre-wrap">
                  {{ course.name }}
                </p>
              </router-link>
              <p v-if="course.objectives.length < descriptionMax">{{ course.objectives }}</p>
              <p v-else>{{ course.objectives.substring(0, descriptionMax) + "..." }}</p>
            </div>
          </div>
          <v-pagination v-model="page" :length="Math.ceil(degree.courses.length / coursesPerPage)" :total-visible="5" />
        </section>

      </article>
    </v-card-text>
  </v-card>

  <!-- Related -->
  <div class="tw-m-10" v-show="related.length > 0">
    <h2 class="tw-text-primary tw-text-2xl">{{ $t('related') }}</h2>
    <v-slide-group show-arrows>
      <v-slide-group-item v-for="degree in related" :key="degree.id">
        <v-card class="tw-m-2" style="width: 300px">
          <v-card-title>
            <h3 class="tw-text-primary tw-text-xl">{{ degree.name }}</h3>
          </v-card-title>
          <v-card-text>
            <p v-if="degree.description.length < 80">{{ degree.description }}</p>
            <p v-else>{{ degree.description.substring(0, 80) + "..." }}</p>
          </v-card-text>
          <v-card-actions>
            <router-link :to="{ params: { id: degree.id } }" :key="degree.id">
              <v-btn variant="text">{{ $t('more') }}</v-btn>
            </router-link>
          </v-card-actions>
        </v-card>
      </v-slide-group-item>
    </v-slide-group>
  </div>
  
</template>
