<template>
  <main class="page">
    <section class="hero">
      <div class="badge">Weather Cache</div>
      <h1>Fast forecasts, cached and ready.</h1>
      <p class="lead">
        Type a city code to pull live weather, then enjoy instant responses
        from Redis the next time.
      </p>
      <form class="search" @submit.prevent="onSubmit">
        <input
          v-model.trim="city"
          type="text"
          placeholder="Try: Berlin, Tokyo, NYC"
          autocomplete="off"
        />
        <button type="submit" :disabled="loading">{{ loading ? 'Loading…' : 'Get Weather' }}</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </section>

    <section class="panel">
      <div class="panel-header">
        <h2>Current snapshot</h2>
        <span class="pill" :class="sourceClass">{{ sourceLabel }}</span>
      </div>

      <div v-if="!data" class="empty">Search for a city to see weather details.</div>

      <div v-else class="grid">
        <div class="card">
          <h3>{{ data.resolvedAddress }}</h3>
          <p class="muted">{{ data.timezone }}</p>
        </div>
        <div class="card">
          <h3>{{ current.temp }}°C</h3>
          <p class="muted">Feels like {{ current.feelslike }}°C</p>
        </div>
        <div class="card">
          <h3>{{ current.conditions }}</h3>
          <p class="muted">Humidity {{ current.humidity }}%</p>
        </div>
        <div class="card">
          <h3>{{ current.windspeed }} km/h</h3>
          <p class="muted">Wind speed</p>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { computed, ref } from 'vue'
import { fetchWeather } from './api'

const city = ref('')
const loading = ref(false)
const error = ref('')
const data = ref(null)
const source = ref('')

const current = computed(() => data.value?.currentConditions || {})

const sourceLabel = computed(() => (source.value ? source.value.toUpperCase() : '—'))
const sourceClass = computed(() => (source.value === 'cache' ? 'cache' : 'live'))

async function onSubmit() {
  error.value = ''
  data.value = null
  source.value = ''

  if (!city.value) {
    error.value = 'Please enter a city name or code.'
    return
  }

  loading.value = true
  try {
    const result = await fetchWeather(city.value)
    data.value = result.data
    source.value = result.source
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>
