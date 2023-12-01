<script setup lang="ts">
defineProps(['modelValue'])
defineEmits(['update:modelValue'])

</script>

<template>
    <v-text-field 
        :label="$t('search')"
        :value="modelValue" 
        :autofocus="true"
        @update:model-value="$emit('update:modelValue', $event)"
        variant="solo"
        append-inner-icon="mdi-magnify"
        >
    </v-text-field>
</template>