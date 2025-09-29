<template>
  <div class="overflow-x-auto">
    <div class="flex justify-between items-center mb-4">
      <div class="flex items-center space-x-4">
        <div class="relative">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Cerca..."
            class="pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <span class="absolute left-3 top-2.5 text-gray-400">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </span>
        </div>
        <select
          v-model="itemsPerPage"
          class="border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="10">10 per pagina</option>
          <option value="25">25 per pagina</option>
          <option value="50">50 per pagina</option>
        </select>
      </div>
      <slot name="table-actions"></slot>
    </div>

    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th
            v-for="column in columns"
            :key="column.key"
            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
            @click="sortBy(column.key)"
          >
            <div class="flex items-center">
              {{ column.label }}
              <span v-if="sortKey === column.key" class="ml-2">
                {{ sortOrder === 'asc' ? '↑' : '↓' }}
              </span>
            </div>
          </th>
          <th v-if="actions" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
            Azioni
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="item in paginatedData" :key="item.id" class="hover:bg-gray-50">
          <td
            v-for="column in columns"
            :key="column.key"
            class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
          >
            <slot :name="column.key" :item="item">
              {{ item[column.key] }}
            </slot>
          </td>
          <td v-if="actions" class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
            <slot name="row-actions" :item="item"></slot>
          </td>
        </tr>
        <tr v-if="paginatedData.length === 0">
          <td :colspan="columns.length + (actions ? 1 : 0)" class="px-6 py-4 text-center text-gray-500">
            Nessun dato disponibile
          </td>
        </tr>
      </tbody>
    </table>

    <div class="flex justify-between items-center mt-4">
      <div class="text-sm text-gray-700">
        Mostrando {{ startItem }} a {{ endItem }} di {{ filteredData.length }} elementi
      </div>
      <div class="flex space-x-2">
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="px-4 py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50"
        >
          Precedente
        </button>
        <button
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50"
        >
          Successivo
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'DataTable',
  props: {
    data: {
      type: Array,
      required: true
    },
    columns: {
      type: Array,
      required: true
    },
    actions: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const searchQuery = ref('')
    const sortKey = ref('')
    const sortOrder = ref('asc')
    const currentPage = ref(1)
    const itemsPerPage = ref(10)

    const filteredData = computed(() => {
      let result = [...props.data]

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(item =>
          Object.values(item).some(value =>
            String(value).toLowerCase().includes(query)
          )
        )
      }

      if (sortKey.value) {
        result.sort((a, b) => {
          const aValue = a[sortKey.value]
          const bValue = b[sortKey.value]
          const modifier = sortOrder.value === 'asc' ? 1 : -1

          if (typeof aValue === 'string') {
            return aValue.localeCompare(bValue) * modifier
          }
          return (aValue - bValue) * modifier
        })
      }

      return result
    })

    const paginatedData = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return filteredData.value.slice(start, end)
    })

    const totalPages = computed(() =>
      Math.ceil(filteredData.value.length / itemsPerPage.value)
    )

    const startItem = computed(() =>
      filteredData.value.length === 0 ? 0 : (currentPage.value - 1) * itemsPerPage.value + 1
    )

    const endItem = computed(() =>
      Math.min(currentPage.value * itemsPerPage.value, filteredData.value.length)
    )

    const sortBy = (key) => {
      if (sortKey.value === key) {
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
      } else {
        sortKey.value = key
        sortOrder.value = 'asc'
      }
    }

    return {
      searchQuery,
      sortKey,
      sortOrder,
      currentPage,
      itemsPerPage,
      filteredData,
      paginatedData,
      totalPages,
      startItem,
      endItem,
      sortBy
    }
  }
}
</script>
