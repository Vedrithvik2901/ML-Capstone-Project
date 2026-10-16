
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import Papa from 'papaparse'
import * as XLSX from 'xlsx'

type Track = 'regression' | 'classification' | 'clustering'

interface DatasetInfo {
  name: string
  file: string
  format: 'csv' | 'xlsx'
}

interface DatasetData {
  headers: string[]
  rows: Record<string, unknown>[]
}

const tracks = [
  { id: 'regression', label: 'Regression' },
  { id: 'classification', label: 'Classification' },
  { id: 'clustering', label: 'Clustering' },
] as const

const datasets: Record<Track, DatasetInfo[]> = {
  regression: [
    {
      name: 'Melbourne Housing',
      file: 'Melbourne_housing.csv',
      format: 'csv',
    },
  ],

  classification: [
    {
      name: 'Bank Marketing (Full)',
      file: 'bank-full.csv',
      format: 'csv',
    },
    {
      name: 'Bank Marketing (Sample)',
      file: 'bank.csv',
      format: 'csv',
    },
  ],

  clustering: [
    {
      name: 'Online Retail',
      file: 'Online Retail.xlsx',
      format: 'xlsx',
    },
  ],
}

// State
const activeTrack = ref<Track>('regression')
const selectedDataset = ref('')
const datasetData = ref<DatasetData | null>(null)
const loading = ref(false)
const error = ref('')
const search = ref('')

// Computed values
const availableDatasets = computed(
  () => datasets[activeTrack.value]
)

const showDatasetDropdown = computed(
  () => availableDatasets.value.length > 1
)

const currentDataset = computed(() =>
  availableDatasets.value.find(
    d => d.file === selectedDataset.value
  )
)

const missingCount = computed(() => {
  if (!datasetData.value) return 0

  return datasetData.value.rows.reduce((count, row) => {
    return count + datasetData.value!.headers.filter(
      header =>
        row[header] === null ||
        row[header] === undefined ||
        String(row[header]).trim() === ''
    ).length
  }, 0)
})

const previewRows = computed(() => {
  if (!datasetData.value) return []

  const rows = datasetData.value.rows

  if (!search.value.trim()) {
    return rows.slice(0, 10)
  }

  const query = search.value.toLowerCase()

  return rows.filter(row =>
    datasetData.value!.headers.some(header =>
      String(row[header] ?? '')
        .toLowerCase()
        .includes(query)
    )
  ).slice(0, 10)
})

// Load a selected dataset
async function loadDataset(file: DatasetInfo) {
  loading.value = true
  error.value = ''
  datasetData.value = null
  search.value = ''

  try {
    const url =
      `${import.meta.env.BASE_URL}datasets/${encodeURIComponent(file.file)}`

    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`Could not load ${file.file}`)
    }

    if (file.format === 'csv') {
      const text = await response.text()

      const parsed = Papa.parse<Record<string, unknown>>(text, {
        header: true,
        skipEmptyLines: true,
        dynamicTyping: true,
      })

      datasetData.value = {
        headers: parsed.meta.fields ?? [],
        rows: parsed.data,
      }
    } else {
      const buffer = await response.arrayBuffer()

      const workbook = XLSX.read(buffer, {
        type: 'array',
      })

      const firstSheet =
        workbook.Sheets[workbook.SheetNames[0]]

      const rows = XLSX.utils.sheet_to_json<
        Record<string, unknown>
      >(firstSheet, {
        defval: null,
      })

      datasetData.value = {
        headers: rows.length ? Object.keys(rows[0]) : [],
        rows,
      }
    }
  } catch (err) {
    error.value = err instanceof Error
      ? err.message
      : 'An unexpected error occurred'
  } finally {
    loading.value = false
  }
}

// Automatically load single-dataset tracks
watch(
  [activeTrack, selectedDataset],
  async (newValues, oldValues) => {
    const [track, file] = newValues
    const previousTrack = oldValues?.[0]

    // A track was changed
    if (track !== previousTrack) {
      const trackDatasets = datasets[track]

      // Regression and Clustering have one dataset
      if (trackDatasets.length === 1) {
        selectedDataset.value = trackDatasets[0].file
        return
      }

      // Classification has multiple datasets
      selectedDataset.value = ''
      datasetData.value = null
      search.value = ''
      return
    }

    // No dataset selected
    if (!file) {
      datasetData.value = null
      return
    }

    const dataset = datasets[track].find(
      d => d.file === file
    )

    if (dataset) {
      await loadDataset(dataset)
    }
  },
  { immediate: true }
)
</script>

<template>
  <main class="dataset-page">

    <!-- Page heading -->
    <header class="dataset-header">
      <RouterLink to="/" class="back-link">
        ← Home
      </RouterLink>

      <span class="eyebrow">DATA WORKSPACE</span>

      <h1>Dataset Explorer</h1>

      <p>
        Explore the datasets used across your machine learning project.
      </p>
    </header>

    <!-- Track selection -->
    <nav class="track-tabs">
      <button
        v-for="track in tracks"
        :key="track.id"
        :class="{ active: activeTrack === track.id }"
        @click="activeTrack = track.id"
      >
        {{ track.label }}
      </button>
    </nav>

    <!-- Dataset selection panel -->
    <section class="dataset-toolbar">

      <div class="toolbar-heading">
        <div>
          <span class="section-label">DATA SOURCE</span>
          <h2>Select a dataset</h2>
        </div>

        <span class="track-badge">
          {{ tracks.find(t => t.id === activeTrack)?.label }}
        </span>
      </div>

      <div class="toolbar-controls">

        <!-- Classification: choose between datasets -->
        
<div v-if="showDatasetDropdown" class="control-group">
  <label for="dataset-select">Dataset</label>

  <select
    id="dataset-select"
    v-model="selectedDataset"
    class="dataset-select"
  >
    <option
      v-for="dataset in availableDatasets"
      :key="dataset.file"
      :value="dataset.file"
    >
      {{ dataset.name }}
    </option>
  </select>
</div>


        <!-- Regression and Clustering: automatic dataset -->
        <div v-else class="control-group">
          <label>Dataset</label>

          <div class="dataset-name-display">
            {{ availableDatasets[0]?.name }}
          </div>
        </div>

        <!-- Search rows -->
        <div class="control-group search-control">
          <label for="dataset-search">Search rows</label>

          <input
            id="dataset-search"
            v-model="search"
            type="search"
            class="dataset-search"
            placeholder="Search across all columns..."
            :disabled="!datasetData"
          />
        </div>

      </div>
    </section>

    <!-- Loading state -->
    <section v-if="loading" class="status-panel">
      <span class="loading-indicator"></span>
      <p>Loading dataset...</p>
    </section>

    <!-- Error state -->
    <section
      v-else-if="error"
      class="status-panel error-state"
    >
      <h2>Unable to load dataset</h2>
      <p>{{ error }}</p>
    </section>

    <!-- Dataset content -->
    <template v-else-if="datasetData">

      <!-- Dataset title -->
      <div class="dataset-title-row">
        <div>
          <span class="section-label">CURRENT DATASET</span>

          <h2>{{ currentDataset?.name }}</h2>

          <p class="dataset-filename">
            {{ currentDataset?.file }}
          </p>
        </div>

        <span class="file-badge">
          {{ currentDataset?.format?.toUpperCase() }}
        </span>
      </div>

      <!-- Statistics -->
      <section class="dataset-stats">

        <article class="stat-card">
          <span class="stat-label">Total rows</span>

          <strong>
            {{ datasetData.rows.length.toLocaleString() }}
          </strong>

          <span class="stat-description">
            Records in dataset
          </span>
        </article>

        <article class="stat-card">
          <span class="stat-label">Total columns</span>

          <strong>
            {{ datasetData.headers.length.toLocaleString() }}
          </strong>

          <span class="stat-description">
            Available features
          </span>
        </article>

        <article class="stat-card">
          <span class="stat-label">Missing values</span>

          <strong>
            {{ missingCount.toLocaleString() }}
          </strong>

          <span class="stat-description">
            Empty or unavailable cells
          </span>
        </article>

      </section>

      <!-- Dataset preview -->
      <section class="dataset-preview">

        <div class="preview-header">
          <div>
            <span class="section-label">DATA PREVIEW</span>

            <h2>Dataset records</h2>

            <p class="preview-note">
              Showing {{ previewRows.length }} of up to 10 matching records.
            </p>
          </div>
        </div>

        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th
                  v-for="header in datasetData.headers"
                  :key="header"
                >
                  {{ header }}
                </th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="(row, index) in previewRows"
                :key="index"
              >
                <td
                  v-for="header in datasetData.headers"
                  :key="header"
                >
                  {{ row[header] ?? '—' }}
                </td>
              </tr>

              <tr v-if="previewRows.length === 0">
                <td :colspan="datasetData.headers.length">
                  No matching rows found.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

      </section>

    </template>

    <!-- Initial state -->
    <section v-else class="status-panel">
      <h2>Choose a dataset to begin</h2>

      <p>
        Select a dataset above to view its statistics and records.
      </p>
    </section>

  </main>
</template>
