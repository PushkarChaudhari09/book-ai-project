import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from books.models import Book

file_path = "books.csv"

added = 0
skipped = 0

with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        title = row['title'].strip()

        # ✅ EXACT DUPLICATE CHECK
        if Book.objects.filter(title__iexact=title).exists():
            print(f"Skipped duplicate: {title}")
            skipped += 1
            continue

        # ✅ CREATE BOOK
        Book.objects.create(
            title=title,
            author=row['author'],
            description=row['description'],
            rating=float(row['rating']),
            url=row['url'],
            summary="Sample summary"
        )

        print(f"Added: {title}")
        added += 1

print("\nDONE ✅")
print(f"Added: {added}")
print(f"Skipped: {skipped}")