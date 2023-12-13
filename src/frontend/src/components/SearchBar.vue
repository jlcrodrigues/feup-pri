<script setup lang="ts">
defineProps(['modelValue'])
defineEmits(['update:modelValue', 'clickIcon'])

</script>

<template>
    <v-text-field 
        :label="$t('search')"
        :value="modelValue" 
        :autofocus="true"
        @update:model-value="$emit('update:modelValue', $event)"
        variant="solo"
        append-inner-icon="mdi-magnify"
        @click:append-inner="$emit('clickIcon')"
        >
    </v-text-field>
</template>