from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

# ================= BASIC CRUD =================

@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_book(request, pk):
    try:
        book = Book.objects.get(id=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"})


@api_view(['POST'])
def add_book(request):
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


# ================= AI FEATURES =================

# TEMP SIMPLE VERSION (no AI crash)



def generate_answer(context, question):
    try:
        from openai import OpenAI
        import os
        from dotenv import load_dotenv

        load_dotenv()

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful book assistant."},
                {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", e)

        # ✅ FALLBACK (ALWAYS WORKS)
        return f"📚 Based on available books:\n\n{context[:500]}"
@api_view(['GET'])
def get_recommendations(request, book_id):
    return Response({
        "recommendations": [
            "Sample Book 1",
            "Sample Book 2",
            "Sample Book 3"
        ]
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def ask_question(request):
    question = request.data.get("question")

    if not question:
        return Response({"answer": "Please ask something."})

    try:
        # 🔍 Try RAG first
        from .rag import query_books
        results = query_books(question)

        if results:
            answer = "📚 Based on your query:\n\n"
            for i, r in enumerate(results):
                answer += f"{i+1}. {r}\n\n"
            return Response({"answer": answer})

    except Exception as e:
        print("RAG ERROR:", e)

    # 🔥 FALLBACK 1 → DATABASE SEARCH
    try:
        from .models import Book

        books = Book.objects.filter(title__icontains=question)

        if books.exists():
            answer = "📚 Books found:\n\n"
            for i, b in enumerate(books[:5]):
                answer += f"{i+1}. {b.title} - {b.description}\n\n"
            return Response({"answer": answer})

    except Exception as e:
        print("DB ERROR:", e)

    # 🔥 FINAL FALLBACK (NEVER FAIL)
    return Response({
        "answer": f"📚 No AI available, but you searched for: '{question}'"
    })