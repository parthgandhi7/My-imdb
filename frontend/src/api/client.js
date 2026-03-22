const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `HTTP ${response.status}`);
  }

  return response.status === 204 ? null : response.json();
}

export const api = {
  listMovies: () => request("/movies"),
  listWatchlist: () => request("/movies/watchlist"),
  listHistory: () => request("/movies/history"),
  addMovie: (payload) => request("/movies", { method: "POST", body: JSON.stringify(payload) }),
  updateMovie: (movieId, payload) => request(`/movies/${movieId}`, { method: "PATCH", body: JSON.stringify(payload) }),
  toggleWatched: (movieId) => request(`/movies/${movieId}/toggle-watched`, { method: "POST" }),
  likeMovie: (movieId) => request(`/movies/${movieId}/like`, { method: "POST" }),
  dislikeMovie: (movieId) => request(`/movies/${movieId}/dislike`, { method: "POST" }),
  agentSearch: (payload) => request("/agent/search", { method: "POST", body: JSON.stringify(payload) }),
};
