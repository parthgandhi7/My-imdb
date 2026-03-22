export function MovieCard({ movie, onToggleWatched, onLike, onDislike }) {
  const providers = movie.providers?.length ? movie.providers.join(", ") : "Unknown";

  return (
    <article className="movie-card">
      <div className="movie-header">
        <h3>
          {movie.title} {movie.release_year ? `(${movie.release_year})` : ""}
        </h3>
        <span className={`sentiment ${movie.sentiment}`}>{movie.sentiment}</span>
      </div>
      <p className="providers">OTT: {providers}</p>
      {movie.overview ? <p className="overview">{movie.overview}</p> : null}
      <div className="actions">
        <button onClick={() => onToggleWatched(movie.id)}>
          Mark as {movie.watched ? "Unwatched" : "Watched"}
        </button>
        <button className="like" onClick={() => onLike(movie.id)}>
          Like
        </button>
        <button className="dislike" onClick={() => onDislike(movie.id)}>
          Dislike
        </button>
      </div>
    </article>
  );
}
