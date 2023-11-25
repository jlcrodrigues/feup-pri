import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

const useApiStore = defineStore('api', () => {
  // get url from .env.dev
  const url = ref(import.meta.env.VITE_BACKEND_URI)

  return { url }
})

export default useApiStore
