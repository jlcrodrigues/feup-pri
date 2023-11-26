<script setup lang="ts">
import { ref } from 'vue'
import { VTextField } from 'vuetify/components';
import useApiStore from '@/stores/store'
import Degree from '@/model/customTypes'
import { useRoute } from 'vue-router';
import { watch } from 'fs';
import { onBeforeMount } from 'vue';
import { onMounted } from 'vue';

const route = useRoute()
const id = ref(route.query.id as string)

const degree = ref({} as Degree)

const getDegree = async () => {
  const response = await fetch(`${useApiStore().url}/degree?id=${id.value}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/text'
    },
  })
  const results = await response.json()
  degree.value = results
}

onMounted(() => {
  getDegree()
})

</script>

<template>
  <v-card class="tw-m-10">
    <v-card-title>
      <div class="tw-flex tw-justify-start tw-gap- tw-items-baseline">
        <h2 class="tw-text-primary tw-text-3xl">{{ degree.name }}</h2>
        <v-btn variant="text" density="compact" :href="degree.url" target="_blank">
          <v-icon class="tw-text-secondary">mdi-open-in-new</v-icon>
        </v-btn>
      </div>
      <div class="tw-flex tw-text-lg tw-text-secondary-light tw-font-light tw-items-center">
        <span>{{ degree.duration }}</span>
        <span class="tw-ml-2 tw-text-primary-lighth tw-font-normal tw-bg-background tw-px-2.5 tw-rounded">{{ degree.type_of_course }}</span>
      </div>
    </v-card-title>
    <v-card-text>
      <article>
        <section class="tw-mb-5">
          {{ degree.description }}
        </section>
        <section>
          <h5 class="tw-text-2xl tw-text-secondary">Saídas Profissionais</h5>
          <p>{{ degree.outings }}</p>
        </section>
      </article>
    </v-card-text>
  </v-card>
</template>
