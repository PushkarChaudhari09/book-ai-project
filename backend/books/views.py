from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

# ================= BASIC =================

@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    return Response(BookSerializer(books, many=True).data)


@api_view(['GET'])
def get_book(request, pk):
    try:
        book = Book.objects.get(id=pk)
        return Response(BookSerializer(book).data)
    except:
        return Response({"error": "Not found"})


@api_view(['GET', 'POST'])
def add_book(request):

    if request.method == 'GET':
        return Response({
            "message": "Use POST to add a book",
            "example": {
                "title": "Harry Potter",
                "author": "J.K Rowling",
                "description": "Wizard story",
                "rating": 4.9
            }
        })

    from .rag import add_book_to_vector

    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        book = serializer.save()
        add_book_to_vector(book)

        return Response({
            "message": "Book added successfully",
            "data": serializer.data
        })

    return Response(serializer.errors)


# ================= AI =================

@api_view(['GET', 'POST'])
def ask_question(request):

    if request.method == 'GET':
        return Response({
            "message": "Use POST",
            "example": {"question": "Harry Potter"}
        })

    from .rag import query_books

    question = request.data.get("question")

    if not question:
        return Response({"error": "Please provide a question"})

    try:
        results = query_books(question)

        if not results:
            return Response({"answer": "No relevant books found."})

        text = results[0]

        # 🔥 MAKE HUMAN-LIKE SENTENCE
        words = text.split()

        if len(words) >= 3:
            title = words[0] + " " + words[1]
            description = " ".join(words[2:])
        else:
            title = text
            description = ""

        answer = f"{title} is a book about {description.lower()}."

        # optional enhancement
        if "wizard" in text.lower():
            answer += " It belongs to the fantasy genre."

        return Response({
            "question": question,
            "answer": answer
        })

    except Exception as e:
        print("ERROR:", e)
        return Response({
            "answer": "Something went wrong"
        })
# 🔥 RECOMMENDATION
@api_view(['GET'])
def get_recommendations(request, book_id):
    from .rag import recommend_books

    try:
        recs = recommend_books(book_id)
        return Response({"recommendations": recs})
    except:
        return Response({"recommendations": []})


# 🔥 SUMMARY
@api_view(['GET', 'POST'])
def generate_summary_view(request):

    if request.method == 'GET':
        return Response({
            "message": "Use POST",
            "example": {"text": "Book description"}
        })

    from .ai import generate_summary

    text = request.data.get("text")
    summary = generate_summary(text)

    return Response({"summary": summary})


# 🔥 GENRE
@api_view(['GET', 'POST'])
def classify_genre(request):

    if request.method == 'GET':
        return Response({
            "message": "Use POST",
            "example": {"description": "Wizard story"}
        })

    from .ai import classify_genre

    desc = request.data.get("description")
    genre = classify_genre(desc)

    return Response({"genre": genre})


# 🔥 CSV UPLOAD
@api_view(['GET', 'POST'])
def upload_books(request):

    if request.method == 'GET':
        return Response({
            "message": "Upload CSV using POST"
        })

    import csv

    file = request.FILES['file']
    decoded = file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded)

    for row in reader:
        Book.objects.create(
            title=row['title'],
            author=row['author'],
            description=row['description'],
            rating=row['rating']
        )

    return Response({"message": "Books uploaded successfully"})