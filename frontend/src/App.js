import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const API = "http://127.0.0.1:8000/api";

  const [books, setBooks] = useState([]);
  const [search, setSearch] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    const res = await axios.get(`${API}/books/`);
    setBooks(res.data);
  };

  const askQuestion = async () => {
    const res = await axios.post(`${API}/ask/`, { question });
    setAnswer(res.data.answer);
  };

  const getRecommendations = async (id) => {
    const res = await axios.get(`${API}/recommend/${id}/`);
    setRecommendations(res.data.recommendations);
  };

  const filteredBooks = books.filter((b) =>
    b.title.toLowerCase().startsWith(search.toLowerCase())
  );

  return (
    <div className="app">
      
      {/* NAVBAR */}
      <div className="navbar">
        <h2>📚 BookAI</h2>
        <input
          type="text"
          placeholder="Search books..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* SEARCH DROPDOWN */}
      {search && (
        <div className="dropdown">
          {filteredBooks.slice(0, 5).map((b) => (
            <div key={b.id}>{b.title}</div>
          ))}
        </div>
      )}

      {/* HERO */}
      <div className="hero">
        <h1>Discover Books with AI</h1>

        <div className="askBox">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask anything..."
          />
          <button onClick={askQuestion}>Ask</button>
        </div>

        {answer && <div className="answer">{answer}</div>}
      </div>

      {/* BOOK GRID */}
      <h2 className="title">Popular Books</h2>

      <div className="grid">
        {books.map((book) => (
          <div key={book.id} className="card">
            <h3>{book.title}</h3>
            <p className="author">{book.author}</p>
            <p>{book.description}</p>
            <p className="rating">⭐ {book.rating}</p>

            <button onClick={() => getRecommendations(book.id)}>
              View Similar
            </button>
          </div>
        ))}
      </div>

      {/* RECOMMENDATIONS */}
      {recommendations.length > 0 && (
        <>
          <h2 className="title">Recommended</h2>
          <div className="grid">
            {recommendations.map((rec, i) => (
              <div key={i} className="card">
                {rec}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default App;