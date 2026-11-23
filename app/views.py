from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Author, Book


def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # --- АВТОРИ ---
        if action == 'create_author':
            Author.objects.create(
                name=request.POST.get('name'),
                birth_year=int(request.POST.get('birth_year')),
                rating=float(request.POST.get('rating'))
            )
            messages.success(request, 'Автора успішно додано!')

        elif action == 'update_author':
            author = get_object_or_404(Author, id=request.POST.get('author_id'))
            author.name = request.POST.get('name')
            author.birth_year = int(request.POST.get('birth_year'))
            author.rating = float(request.POST.get('rating'))
            author.save()
            messages.success(request, f'Дані автора «{author.name}» оновлено!')

        elif action == 'delete_author':
            author = get_object_or_404(Author, id=request.POST.get('author_id'))
            name = author.name
            author.delete()
            messages.success(request, f'Автора «{name}» та його книги видалено.')

        # --- КНИГИ ---
        elif action == 'create_book':
            author = get_object_or_404(Author, id=request.POST.get('author_id'))
            Book.objects.create(
                title=request.POST.get('title'),
                author=author,
                pages=int(request.POST.get('pages')),
                price=request.POST.get('price'),
                published_year=int(request.POST.get('published_year')),
                stock=int(request.POST.get('stock'))
            )
            messages.success(request, 'Книгу успішно додано!')

        elif action == 'update_book':
            book = get_object_or_404(Book, id=request.POST.get('book_id'))
            book.title = request.POST.get('title')
            book.author = get_object_or_404(Author, id=request.POST.get('author_id'))
            book.pages = int(request.POST.get('pages'))
            book.price = request.POST.get('price')
            book.published_year = int(request.POST.get('published_year'))
            book.stock = int(request.POST.get('stock'))
            book.save()
            messages.success(request, f'Книгу «{book.title}» оновлено!')

        elif action == 'delete_book':
            book = get_object_or_404(Book, id=request.POST.get('book_id'))
            title = book.title
            book.delete()
            messages.success(request, f'Книгу «{title}» видалено.')

        return redirect('index')

    # GET-запит: оптимізоване отримання даних (без проблеми N+1)
    authors = Author.objects.prefetch_related('books').all().order_by('-id')
    books = Book.objects.select_related('author').all().order_by('-id')

    return render(request, 'custom_admin_panel.html', {
        'authors': authors,
        'books': books
    })