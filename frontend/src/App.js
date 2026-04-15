import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const API = "http://127.0.0.1:8000/api";

  const [books, setBooks] = useState([]);
  const [search, setSearch] = useState("");
  const [selectedBook, setSelectedBook] = useState(null);

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

  // 🔍 SEARCH FIX
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

      {/* 🔍 SEARCH DROPDOWN */}
      {search && !selectedBook && (
        <div className="dropdown">
          {filteredBooks.slice(0, 5).map((b) => (
            <div
              key={b.id}
              className="dropdown-item"
              onClick={() => {
                setSelectedBook(b);
                setSearch("");
                setAnswer("");
                setRecommendations([]);
              }}
            >
              🔍 {b.title}
            </div>
          ))}
        </div>
      )}

      {/* 📘 BOOK DETAIL PAGE */}
      {selectedBook ? (
        <div className="detail">

          <button className="back-btn" onClick={() => setSelectedBook(null)}>
            ⬅ Back
          </button>

          <h1>{selectedBook.title}</h1>
          <h3>{selectedBook.author}</h3>

          <p className="desc">{selectedBook.description}</p>
          <p className="rating">⭐ {selectedBook.rating}</p>

          {/* 🤖 AI SECTION */}
          <div className="askBox">
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask about this book..."
            />
            <button onClick={askQuestion}>Ask AI</button>
          </div>

          {answer && <div className="answer">{answer}</div>}

          {/* 📚 RECOMMENDATIONS */}
          <button onClick={() => getRecommendations(selectedBook.id)}>
            Get Recommendations
          </button>

          {recommendations.length > 0 && (
            <div className="grid">
              {recommendations.map((rec, i) => (
                <div key={i} className="card">{rec}</div>
              ))}
            </div>
          )}
        </div>
      ) : (
        <>
          {/* HERO */}
          <div className="hero">
            <h1>Discover Books with AI</h1>
          </div>

          {/* 🔍 SEARCH RESULTS */}
          {search && (
            <>
              <h2 className="title">Search Results</h2>

              <div className="grid">
                {filteredBooks.slice(0, 10).map((book) => (
                  <div
                    key={book.id}
                    className="card"
                    onClick={() => setSelectedBook(book)}
                  >
                    <h3>{book.title}</h3>
                    <p>{book.author}</p>
                    <p>⭐ {book.rating}</p>
                  </div>
                ))}
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
}

export default App;