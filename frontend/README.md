###BookAI – Document Intelligence Platform

A full-stack AI-powered book discovery platform built using Django REST Framework + ReactJS with a RAG (Retrieval-Augmented Generation) pipeline.

##Features

- Google-like live book search
- Book detail page
- AI-based question answering (RAG)
- Book summary generation
- Book recommendations
- REST API backend
- Fast and responsive UI

##Tech Stack

- ReactJS
- Django REST Framework
- SQLite
- Custom RAG + OpenAI (optional fallback)
- ChromaDB
- CSV-based ingestion

##Screenshots

#1. Home Page

- C:\Users\pushk\book_ai_project\frontend\Scrreenshots\Home.png.png

#2. Search Results

- C:\Users\pushk\book_ai_project\frontend\Scrreenshots\Search.png

#3. Book Detail Page

- C:\Users\pushk\book_ai_project\frontend\Scrreenshots\Book Details.png

#4. AI Response

- C:\Users\pushk\book_ai_project\frontend\Scrreenshots\AI Response.png

##Setup Instructions

#1. Backend Setup

    cd backend

    python -m venv venv 
    venv\Scripts\activate 

    pip install -r requirements.txt

    python manage.py migrate 
    python manage.py runserver

#2. Frontend Setup

    cd frontend

    npm install 
    npm start

##API Documentation

#1. GET APIs

    /api/books/ → Get all books
    /api/books/<id>/ → Get single book
    /api/recommend/<id>/ → Get recommendations

#2. POST APIs

    /api/ask/ → Ask AI question
    /api/summary/ → Generate summary
    /api/books/add/ → Add book
    /api/upload/ → Upload CSV

##Sample Questions & Answers

#1. Sample Questions & Answers
- A fantasy story about a young wizard discovering magic, friendship, and courage.

#2. Recommend books like Atomic Habits
- Deep Work, Think and Grow Rich, The Power of Now.


