<script setup lang="ts">
import { ref } from 'vue';

const isOpen = ref(false);

const props = defineProps({ name: String, list: Array<string>, criteria: { type: String }, order: { type: String, default: 'asc' } });
const emits = defineEmits(['update', 'update:criteria', 'update:order']);

const updateKeyValue = (value: string | null) => {
    emits('update:criteria', value)
    emits('update')
}

const reset = () => {
    if (props.criteria == null || props.criteria == "") return
    emits('update:criteria', null)
    emits('update')
}

const updateOrderValue = (value: string | null) => {
    emits('update:order', value)
    emits('update')
}

</script>

<template>
    <v-menu v-model="isOpen" location="bottom" transition="slide-y-transition" :close-on-content-click="false">
        <template v-slot:activator="{ props }">
            <v-chip v-bind="props" :variant="(criteria == null || criteria == '') ? 'tonal' : 'elevated'"
                prepend-icon="mdi-sort-variant">{{ name
                }}</v-chip>
        </template>

        <v-list>
            <h5 class="tw-m-2 tw-font-bold tw-text-primary">{{ $t('sortKey') }}</h5>
            <v-radio-group :model-value="criteria" @update:model-value="updateKeyValue">
                <v-list-item>
                    <v-radio v-for="(item, index) in list" :key="index" :label="$t(item)" :value="item" density="compact"
                        @click="reset()">
                    </v-radio>
                </v-list-item>
            </v-radio-group>
            <h5 class="tw-m-2 tw-font-bold tw-text-primary">{{ $t('sortOrder') }}</h5>
            <v-btn-toggle :model-value="order" @update:model-value="updateOrderValue" mandatory variant="text"
                class="tw-m-2">
                <v-btn icon="mdi-arrow-up" value="asc"></v-btn>
                <v-btn icon="mdi-arrow-down" value="desc"></v-btn>
            </v-btn-toggle>
        </v-list>
    </v-menu>
</template>