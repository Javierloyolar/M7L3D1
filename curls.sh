# ============================================================
# 1. LISTAR LIBROS (READ)
# ============================================================

curl http://127.0.0.1:8000/api/books/


# ============================================================
# 2. CREAR AUTORES
# (RELACIÓN UNO A MUCHOS: Autor → Libros)
# ============================================================

curl -X POST http://127.0.0.1:8000/api/authors/create/ \
-H "Content-Type: application/json; charset=utf-8" \
-d '{
  "name": "Gabriel Garcia Marquez",
  "birth_date": "1927-03-06"
}'


curl -X POST http://127.0.0.1:8000/api/authors/create/ \
-H "Content-Type: application/json; charset=utf-8" \
-d '{
  "name": "Isabel Allende",
  "birth_date": "1942-08-02"
}'


# ============================================================
# 3. CREAR LIBROS
# - MANY TO ONE  (Libro → Autor)
# - MANY TO MANY (Libro ↔ Categorias)
# - ENTIDAD INTERMEDIA: BookCategory (priority)
# ============================================================

curl -X POST http://127.0.0.1:8000/api/books/create/ \
-H "Content-Type: application/json; charset=utf-8" \
-d '{
  "title": "Cien Anos de Soledad",
  "isbn": "9788439720810",
  "author_id": 1,
  "published_date": "1967-05-30",
  "categories": [
    { "name": "Realismo Magico", "priority": 1 },
    { "name": "Literatura Latinoamericana", "priority": 2 }
  ]
}'


curl -X POST http://127.0.0.1:8000/api/books/create/ \
-H "Content-Type: application/json; charset=utf-8" \
-d '{
  "title": "La Casa de los Espiritus",
  "isbn": "9788401352836",
  "author_id": 2,
  "published_date": "1982-01-01",
  "categories": [
    { "name": "Realismo Magico", "priority": 1 },
    { "name": "Novela", "priority": 2 }
  ]
}'


# ============================================================
# 4. LISTAR LIBROS CON RELACIONES NAVEGADAS
# - Autor (FK)
# - Categorias (M2M)
# ============================================================

curl http://127.0.0.1:8000/api/books/