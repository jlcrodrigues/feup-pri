<script setup lang="ts">
import { ref } from 'vue'
import { VTextField } from 'vuetify/components';
import Degree from '@/model/customTypes'
import { useRoute } from 'vue-router';
import { watch } from 'fs';

const route = useRoute()
const id = ref(route.query.id as string)


const getDegree = async () => {
  // TODO: query degree from db
}

</script>

<template>
  This is the degree #{{ id }} page.
</template>
