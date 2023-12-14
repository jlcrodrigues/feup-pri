<script setup lang="ts">
import { ref, watch } from 'vue'
import { VTextField } from 'vuetify/components';
import useApiStore from '@/stores/api'
import Professor from '@/model/types'
import { useRoute, useRouter } from 'vue-router';
import { onBeforeMount } from 'vue';
import { onMounted } from 'vue';

const router = useRouter()
const route = useRoute()
const id = ref(route.params.id as string)

const professor = ref({} as Professor)
const related = ref([] as Professor[])

const apiStore = useApiStore()
onMounted(async () => {
  professor.value = await apiStore.getProfessor(id.value)
  getRelated()
})

const getRelated = async () => {
  related.value = await apiStore.getRelatedProfessors(id.value)
}

watch(() => route.params.id, () => {
  router.go(0)
})

const contents = ['personalPresentation', 'fieldsOfInterest']

const copyEmail = () => {
  navigator.clipboard.writeText(professor.value.institutionalEmail)
}

const copyPhone = () => {
  navigator.clipboard.writeText(professor.value.phone)
}

</script>

<template>
  <v-card class="tw-m-10">
    <v-card-title>
      <div class="tw-flex tw-justify-start tw-gap- tw-items-baseline">
        <h2 class="tw-text-primary tw-text-3xl">{{ professor.name }}</h2>
        <v-btn variant="text" density="compact" v-if="professor.institutionalWebsite" :href="professor.institutionalWebsite" target="_blank">
          <v-icon class="tw-text-secondary">mdi-open-in-new</v-icon>
        </v-btn>
      </div>
      <div class="tw-flex tw-text-lg tw-text-secondary-light tw-font-light tw-items-center">
        <span>{{ professor.rank }}</span>
        <span class="tw-ml-2 tw-text-primary-lighth tw-font-normal tw-bg-background tw-px-2.5 tw-rounded">{{
          professor.abbreviation
        }} </span>
        <span class="tw-ml-2 tw-italic">{{ professor.status }}</span>
      </div>
    </v-card-title>
    <v-card-text>
      <div class="tw-flex tw-items-baseline" v-if="professor.institutionalEmail">
        <v-icon class="tw-text-secondary" size="large">mdi-email-outline</v-icon>
        <a class="tw-ml-2 tw-text-lg" :href="`mailto:${professor.institutionalEmail}`">{{ professor.institutionalEmail }}</a>
        <v-btn variant="plain">
          <v-icon @click="copyEmail()">mdi-content-copy</v-icon>
        </v-btn>
      </div>
      <div class="tw-flex tw-items-center" v-if="professor.phone">
        <v-icon class="tw-text-secondary" size="large">mdi-phone-outline</v-icon>
        <span class="tw-ml-2 tw-text-lg">{{ professor.phone }}</span>
        <v-btn variant="plain">
          <v-icon @click="copyPhone()">mdi-content-copy</v-icon>
        </v-btn>
      </div>
      <article>
        <section v-for="content in contents" :key="content" class="tw-mt-5">
          <template v-if="professor[content]">
            <h5 class="tw-text-2xl tw-text-secondary">{{ $t(content) }}</h5>
            <p class="tw-whitespace-pre-wrap">{{ professor[content] }}</p>
          </template>
        </section>
      </article>
    </v-card-text>
  </v-card>

  <!-- Related -->
  <div class="tw-m-10" v-show="related.length > 0">
    <h2 class="tw-text-primary tw-text-2xl">{{ $t('related') }}</h2>
    <v-slide-group show-arrows>
      <v-slide-group-item v-for="professor in related" :key="professor.id">
        <v-card class="tw-m-2" style="width: 300px;">
          <v-card-title>
            <h3 class="tw-text-primary tw-text-xl">{{ professor.name }}</h3>
          </v-card-title>
          <v-card-text>
            <p v-if="professor.personalPresentation.length < 80">{{ professor.personalPresentation }}</p>
            <p v-else>{{ professor.personalPresentation.substring(0, 80) + "..." }}</p>
          </v-card-text>
          <v-card-actions>
            <router-link :to="{ params: { id: professor.id } }" :key="professor.id">
              <v-btn variant="text">{{ $t('more') }}</v-btn>
            </router-link>
          </v-card-actions>
        </v-card>
      </v-slide-group-item>
    </v-slide-group>
  </div>
</template>
