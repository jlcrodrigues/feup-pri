<script setup lang="ts">
import { ref, watch } from 'vue'
import { VTextField } from 'vuetify/components';
import useApiStore from '@/stores/api'
import Course from '@/model/types'
import { useRoute, useRouter } from 'vue-router';
import { onBeforeMount } from 'vue';
import { onMounted } from 'vue';
import useEntityStore from '@/stores/entitities';

const entityStore = useEntityStore()

const router = useRouter()
const route = useRoute()
const id = ref(route.params.id as string)

const course = ref({} as Course)
const related = ref([] as Course[])

const apiStore = useApiStore()

onMounted(async () => {
  course.value = await apiStore.getCourse(id.value)
  getRelated()
  loadEntities();
})

const getRelated = async () => {
  related.value = await apiStore.getRelatedCourses(id.value)
}

watch(() => route.params.id, () => {
  router.go(0)
})

const contents = ['objectives', 'results', 'workingMethod', 'preRequirements', 'program', 'evaluationType', 'passingRequirements']

const loadEntities = async () => {
  course.value = await entityStore.replaceCourseEntities(course.value)
}

</script>

<template>
  <v-card class="tw-m-10">
    <v-card-title>
      <div class="tw-flex tw-justify-start tw-gap- tw-items-baseline">
        <h2 class="tw-text-primary tw-text-3xl">{{ course.name }}</h2>
        <v-btn v-if="course.url" variant="text" density="compact" :href="course.url" target="_blank">
          <v-icon class="tw-text-secondary">mdi-open-in-new</v-icon>
        </v-btn>
      </div>
      <div class="tw-flex tw-text-lg tw-text-secondary-light tw-font-light tw-items-center">
        <span>{{ course.language }}</span>
        <span v-if="course.ects" class="tw-ml-2 tw-text-primary-lighth tw-font-normal tw-bg-background tw-px-2.5 tw-rounded">{{ course.ects
        }} ECTS</span>
      </div>
    </v-card-title>
    <v-card-text>
      <article>
        <section v-for="content in contents" :key="content" class="tw-mt-5">
          <template v-if="course[content]">
            <h5 class="tw-text-2xl tw-text-secondary">{{ $t(content) }}</h5>
            <p class="tw-whitespace-pre-wrap" v-html="course[content]"></p>
          </template>
        </section>
      </article>
    </v-card-text>
  </v-card>

  <!-- Related -->
  <div class="tw-m-10" v-show="related.length > 0">
    <h2 class="tw-text-primary tw-text-2xl">{{ $t('related') }}</h2>
    <v-slide-group show-arrows>
      <v-slide-group-item v-for="course in related" :key="course.id">
        <v-card class="tw-m-2" style="width: 300px;">
          <v-card-title>
            <h3 class="tw-text-primary tw-text-xl">{{ course.name }}</h3>
          </v-card-title>
          <v-card-text>
            <p v-if="course.objectives.length < 80">{{ course.objectives }}</p>
            <p v-else>{{ course.objectives.substring(0, 80) + "..." }}</p>
          </v-card-text>
          <v-card-actions>
            <router-link :to="{ params: { id: course.id } }" :key="course.id">
              <v-btn variant="text">{{ $t('more') }}</v-btn>
            </router-link>
          </v-card-actions>
        </v-card>
      </v-slide-group-item>
    </v-slide-group>
  </div>
</template>
