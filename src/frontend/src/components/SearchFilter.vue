<script setup lang="ts">
import { ref } from 'vue';

const isOpen = ref(false);

defineProps({ name: String, list: Array<string>, modelValue: { type: Array<string>, default: [] } });
const emits = defineEmits(['update:modelValue']);

const updateModelValue = (value: Array<string>) => {
    emits('update:modelValue', value)
}

</script>

<template>
    <v-menu v-model="isOpen" location="bottom" transition="slide-y-transition" :close-on-content-click="false">
        <template v-slot:activator="{ props }">
            <v-chip v-bind="props" :variant="(modelValue.length == 0) ? 'tonal' : 'elevated'">{{ name }}</v-chip>
        </template>

        <v-list>
            <v-list-item v-for="(item, index) in list" :key="index">
                <v-checkbox :model-value="modelValue" @update:model-value="updateModelValue"
                    :label="item" :value="item" density="compact"></v-checkbox>
            </v-list-item>
        </v-list>
    </v-menu>
</template>