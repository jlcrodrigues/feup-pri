<script setup lang="ts">

const links = [
  {
    name: 'degrees',
    path: '/search/degrees'
  },
  {
    name: 'courses',
    path: '/search/courses'
  },
  {
    name: 'professors',
    path: '/search/professors'
  }
]

</script>


<template>
  <header class="tw-bg-background tw-border-b-1 tw-p-2 tw-py-4 tw-shadow-xl">
    <nav class="tw-flex tw-items-baseline tw-justify-end tw-gap-5">
      <a href="/">
        <h3 class="tw-font-medium tw-text-2xl ml-2"><span class="text-secondary">Academic</span><span
            class="tw-text-primary">Quest</span></h3>
      </a>
      <a v-for="link in links" :key="link.name" :href="link.path">
        <h6 class="tw-text-secondary-light tw-text-xl tw-font-extralight">{{ $t(link.name) }}</h6>
      </a>
      <div class="locale-changer tw-justify-end tw-flex tw-grow tw-gap-1 tw-mr-2">
        <v-btn variant="text" density="compact" :color="($i18n.locale == 'en') ? 'primary' : 'secondary'" class="tw-font-bold"
          @click="() => $i18n.locale = 'en'">EN</v-btn>
        |
        <v-btn variant="text" density="compact" :color="($i18n.locale == 'pt') ? 'primary' : 'secondary'" class="tw-font-bold"
          @click="() => $i18n.locale = 'pt'">PT</v-btn>
      </div>
    </nav>
  </header>
</template>