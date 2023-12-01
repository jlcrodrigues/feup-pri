<script setup lang="ts">

const links = [
  {
    name: 'Degrees',
    path: '/search/degrees'
  },
  {
    name: 'Courses',
    path: '/search/courses'
  },
  {
    name: 'Professors',
    path: '/professors'
  }
]

</script>


<template>
  <header class="tw-bg-background tw-border-b-1 tw-p-2 tw-py-4 tw-shadow-xl">
    <nav class="tw-flex tw-items-baseline tw-gap-5">
    <a href="/">
      <h3 class="tw-font-medium tw-text-2xl ml-2"><span class="text-secondary">Academic</span><span
          class="tw-text-primary">Quest</span></h3>
    </a>
    <a v-for="link in links" :key="link.name" :href="link.path">
      <h6 class="tw-text-secondary-light tw-text-xl tw-font-extralight">{{ link.name }}</h6>
    </a>
</nav>
  </header>
</template>