<script setup lang="ts">

import Degree from '@/model/customTypes'
import type { PropType } from 'vue';

// props

defineProps({
  degree: {
    type: Object as PropType<Degree>,
    required: true
  }
})

</script>

<template>
  <p>{{ degree.name }}</p>
</template>
