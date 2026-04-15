from sentence_transformers import SentenceTransformer
import chromadb

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create DB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="books")


# ✅ ADD BOOK TO VECTOR
def add_book_to_vector(book):
    text = f"{book.title} {book.description} {book.summary}"
    embedding = model.encode(text).tolist()

    collection.add(
        documents=[text],
        ids=[str(book.id)],
        embeddings=[embedding]
    )


# ✅ QUERY BOOKS (MAIN AI SEARCH)
def query_books(question):
    try:
        query_embedding = model.encode(question).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        documents = results.get('documents', [[]])[0]

        if not documents:
            return []

        return documents

    except Exception as e:
        print("RAG ERROR:", e)
        return []