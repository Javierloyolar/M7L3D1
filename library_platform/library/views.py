from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Author,
    Book,
    Category,
    BookCategory
)
import json


def _read_json_body(request):
    """
    Lee el body JSON de forma robusta.

    Problema real en Windows:
    - Algunas consolas/tools envían bytes que no son UTF-8 (cp1252/latin-1),
      especialmente si el texto contiene ñ/á/é/í/ó/ú.
    - json.loads(request.body) intenta detectar y decodificar como UTF-8 -> puede fallar.

    Estrategia:
    1) Intentar UTF-8 estricto (lo correcto para JSON moderno)
    2) Si falla, intentar cp1252 (común en Windows)
    3) Si falla, intentar latin-1 (fallback final)
    4) Si todo falla, devolver error claro (400)
    """
    raw = request.body  # bytes

    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            text = raw.decode(enc)
            return json.loads(text), None
        except UnicodeDecodeError:
            continue
        except json.JSONDecodeError as e:
            return None, f"JSON inválido: {str(e)}"

    return None, "No se pudo decodificar el body (UTF-8/cp1252/latin-1)"


@csrf_exempt
def create_author(request):
    """
    CREATE - Autor (padre de relación uno a muchos)
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    data, err = _read_json_body(request)
    if err:
        return JsonResponse({"error": err}, status=400)

    author = Author.objects.create(
        name=data["name"],
        birth_date=data.get("birth_date")  # ISO: YYYY-MM-DD (string)
    )

    return JsonResponse({"id": author.id, "status": "created"}, status=201)


def list_books(request):
    """
    READ - Libros con navegación de relaciones
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    books = Book.objects.select_related("author").prefetch_related("categories")

    return JsonResponse(
        [
            {
                "id": book.id,
                "title": book.title,
                "isbn": book.isbn,
                "author": {
                    "id": book.author.id,
                    "name": book.author.name,
                },
                "categories": [
                    {
                        "name": c.name,
                    }
                    for c in book.categories.all()
                ],
            }
            for book in books
        ],
        safe=False
    )


@csrf_exempt
def create_book(request):
    """
    CREATE - Libro con relaciones:
    - FK (Book -> Author) muchos a uno
    - M2M (Book <-> Category) con entidad intermedia BookCategory
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    data, err = _read_json_body(request)
    if err:
        return JsonResponse({"error": err}, status=400)

    try:
        author = Author.objects.get(id=data["author_id"])
    except Author.DoesNotExist:
        return JsonResponse({"error": "Author not found"}, status=404)

    book = Book.objects.create(
        title=data["title"],
        isbn=data["isbn"],
        author=author,
        published_date=data.get("published_date")  # ISO: YYYY-MM-DD (string)
    )

    # categories: [{name, priority}]
    for cat in data.get("categories", []):
        category, _ = Category.objects.get_or_create(name=cat["name"])
        BookCategory.objects.create(
            book=book,
            category=category,
            priority=cat.get("priority", 1)
        )

    return JsonResponse({"id": book.id, "status": "created"}, status=201)