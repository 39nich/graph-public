import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useGraphStore = defineStore('graph', () => {
  const graphData = ref<null | Record <string, any>> (null)

  function setGraphData(data:any) {
    graphData.value = data
  }

  function clearGraphData() {
    graphData.value = null
  }

  return {
    graphData,
    setGraphData,
    clearGraphData,
    }
})
