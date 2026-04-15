from sentence_transformers import SentenceTransformer
import chromadb

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create DB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="books")


# ✅ ADD BOOK TO VECTOR
def add_book_to_vector(book):
    text = f"{book.title}. {book.description}."
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
    

def recommend_books(book_id):
    try:
        # get the book from vector DB
        results = collection.get(ids=[str(book_id)])

        if not results or not results['documents']:
            return []

        book_text = results['documents'][0][0]

        # create embedding
        query_embedding = model.encode(book_text).tolist()

        # find similar books
        similar = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )

        recs = similar['documents'][0]

        # remove same book
        return [r for r in recs if r != book_text]

    except Exception as e:
        print("REC ERROR:", e)
        return []