/**
 * API client for the Waypoint RAG pipeline.
 */

/**
 * Submit a query to the RAG pipeline API.
 *
 * @param {string} query - The user's question
 * @param {AbortSignal} signal - AbortController signal for cleanup
 * @returns {Promise<Object>} API response with answer, citations, confidence
 */
export async function submitQuery(query, signal) {
  const response = await fetch('/api/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
    signal,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || `Request failed: ${response.status}`);
  }

  return response.json();
}

/**
 * Check API health status.
 *
 * @returns {Promise<Object>} Health status response
 */
export async function checkHealth() {
  const response = await fetch('/api/health');
  return response.json();
}
