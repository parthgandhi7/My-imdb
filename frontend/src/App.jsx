import { useEffect, useMemo, useState } from "react";

import { api } from "./api/client";
import { MovieCard } from "./components/MovieCard";

const TABS = {
  WATCHLIST: "watchlist",
  HISTORY: "history",
};

function mapSuggestionToMovie(suggestion) {
  const releaseYear = suggestion.release_date ? Number(suggestion.release_date.slice(0, 4)) : null;
  return {
    title: suggestion.title,
    tmdb_id: suggestion.tmdb_id,
    release_year: Number.isNaN(releaseYear) ? null : releaseYear,
    overview: suggestion.overview,
    poster_url: suggestion.poster_url,
    providers: suggestion.providers,
  };
}

export default function App() {
  const [tab, setTab] = useState(TABS.WATCHLIST);
  const [watchlist, setWatchlist] = useState([]);
  const [history, setHistory] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [provider, setProvider] = useState("netflix");
  const [suggestions, setSuggestions] = useState([]);
  const [error, setError] = useState("");

  const loadData = async () => {
    try {
      const [watchlistResponse, historyResponse] = await Promise.all([api.listWatchlist(), api.listHistory()]);
      setWatchlist(watchlistResponse);
      setHistory(historyResponse);
      setError("");
    } catch (loadError) {
      setError(loadError.message);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const activeMovies = useMemo(() => (tab === TABS.WATCHLIST ? watchlist : history), [tab, watchlist, history]);

  const handleToggleWatched = async (movieId) => {
    await api.toggleWatched(movieId);
    await loadData();
  };

  const handleLike = async (movieId) => {
    await api.likeMovie(movieId);
    await loadData();
  };

  const handleDislike = async (movieId) => {
    await api.dislikeMovie(movieId);
    await loadData();
  };

  const handleSearch = async (event) => {
    event.preventDefault();
    if (!prompt.trim()) {
      return;
    }

    try {
      const response = await api.agentSearch({ prompt, provider, limit: 8 });
      setSuggestions(response);
      setError("");
    } catch (searchError) {
      setError(searchError.message);
    }
  };

  const addSuggestion = async (suggestion) => {
    await api.addMovie(mapSuggestionToMovie(suggestion));
    await loadData();
  };

  return (
    <main className="container">
      <header>
        <h1>Movie Tracker</h1>
        <p>Track watchlist/history and discover movies using AI + TMDB.</p>
      </header>

      <section className="agent-box">
        <h2>AI Search Agent</h2>
        <form onSubmit={handleSearch} className="search-form">
          <input
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
            placeholder="Example: A light Bollywood rom-com from 2025"
          />
          <select value={provider} onChange={(event) => setProvider(event.target.value)}>
            <option value="netflix">Netflix</option>
            <option value="prime video">Prime Video</option>
            <option value="disney+">Disney+</option>
            <option value="hulu">Hulu</option>
          </select>
          <button type="submit">Find Movies</button>
        </form>
        <div className="suggestions">
          {suggestions.map((item) => (
            <article key={item.tmdb_id} className="suggestion-card">
              <h3>{item.title}</h3>
              <p>{item.overview || "No overview available."}</p>
              <p>
                OTT: {item.providers?.length ? item.providers.join(", ") : "Unknown"}
              </p>
              <button onClick={() => addSuggestion(item)}>Add to Watchlist</button>
            </article>
          ))}
        </div>
      </section>

      <section className="tabs">
        <button className={tab === TABS.WATCHLIST ? "active" : ""} onClick={() => setTab(TABS.WATCHLIST)}>
          Watchlist
        </button>
        <button className={tab === TABS.HISTORY ? "active" : ""} onClick={() => setTab(TABS.HISTORY)}>
          History
        </button>
      </section>

      {error ? <p className="error">{error}</p> : null}

      <section className="movie-grid">
        {activeMovies.length === 0 ? (
          <p>No movies in this tab yet.</p>
        ) : (
          activeMovies.map((movie) => (
            <MovieCard
              key={movie.id}
              movie={movie}
              onToggleWatched={handleToggleWatched}
              onLike={handleLike}
              onDislike={handleDislike}
            />
          ))
        )}
      </section>
    </main>
  );
}
