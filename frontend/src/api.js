export async function fetchWeather(city) {
  const params = new URLSearchParams({ city })
  const response = await fetch(`/api/weather?${params.toString()}`)
  const data = await response.json()
  if (!response.ok) {
    const message = data?.error || 'Failed to load weather.'
    throw new Error(message)
  }
  return data
}
