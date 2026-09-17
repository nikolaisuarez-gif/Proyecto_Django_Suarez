# Lab 04 — Relaciones de Modelos en Django

**Autor:** Nikolai Alexander Suárez Nuñez — nikolai.suarez@tecsup.edu.pe
**Proyecto:** Proyecto_Django_Suarez (app `library`)
**Repositorio:** https://github.com/nikolaisuarez-gif/Proyecto_Django_Suarez

---

## 1. Instalación de Pillow y configuración de archivos multimedia

Se instaló **Pillow** (requerido por `ImageField`) en el entorno virtual:

```bash
.venv\Scripts\pip install Django==6.1 Pillow
```

En `todoproject/settings.py`:

```python
INSTALLED_APPS = [ ..., 'library' ]

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Y en `todoproject/urls.py` se sirven los medios en modo DEBUG:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

`requirements.txt`:

```
Django==6.1
Pillow==12.3.0
```

---

## 2. Diagrama de modelos (app `library`)

```
                    ┌──────────────────┐
                    │     Author       │
                    │──────────────────│
                    │ name (Char)      │
                    │ email (Email)    │
                    │ birth_date (Date)│
                    └────────┬─────────┘
                             │ 1            FK  related_name="books"  CASCADE
                             ▼
┌──────────────┐   ┌─────────┴─────────┐   ┌──────────────────┐
│  Publisher   │◄──┤       Book        │──►│   Publication    │
│──────────────│   │───────────────────│   │──────────────────│
│ name (Char)  │   │ title (Char)      │   │ title (Char)     │
│ city (Char)  │   │ isbn (unique)     │   │ publication_date │
│ website (URL)│   │ price (Decimal)   │   │ edition          │
└──────────────┘   │ cover (ImageField)│──►│ language / pages │
     FK PROTECT    └─────────▲─────────┘   └──────────────────┘
    related_name   M2M        │ 1               1 OneToOneField
    ="books"                  │                  related_name="book"
                              │                     CASCADE
                 ┌────────────┴─────────────┐
                 │     BookCategory         │  ← modelo intermediario (through)
                 │──────────────────────────│
                 │ book (FK)                │
                 │ category (FK)            │
                 │ is_primary (Bool)        │
                 │ unique (book, category)  │
                 └────────────┬─────────────┘
                              │ 1
                              ▼
                 ┌──────────────────┐
                 │     Category     │
                 │──────────────────│
                 │ name (unique)    │
                 │ description      │
                 └──────────────────┘
```

| Relación | Tipo | `on_delete` | `related_name` |
|----------|------|-------------|----------------|
| `Book.author` → `Author` | ForeignKey | CASCADE | `books` |
| `Book.publisher` → `Publisher` | ForeignKey | PROTECT | `books` |
| `Book.publication` → `Publication` | OneToOneField | CASCADE | `book` |
| `Book.categories` → `Category` | ManyToManyField (through `BookCategory`) | CASCADE (`BookCategory`) | `books` / `book_categories` |

Todos los modelos tienen `class Meta` (orden por nombre/título) y `__str__`.

---

## 3. Migraciones y tablas creadas

```bash
python manage.py makemigrations library
python manage.py migrate
```

Tablas verificadas en la BD (SQLite):

```
library_author       library_book         library_bookcategory
library_category     library_publication  library_publisher
```

La tabla **intermedia** `library_bookcategory` existe gracias al `through="BookCategory"`.

---

## 4. Carga de datos (seed)

Datos cargados con `python manage.py seed_library` (idempotente, usa `get_or_create`):

- **Autores (2):** Gabriel García Márquez, Isabel Allende
- **Editoriales (2):** Random House (Lima), Planeta (Madrid)
- **Categorías (3):** Novela, Realismo mágico, Ficción histórica
- **Libros (4):** Cien años de soledad, El amor en los tiempos del cólera, La casa de los espíritus, Inés del alma mía
- **Publicaciones (4):** una por libro (OneToOne)

Resultado del seed:

```
Autor(es): 2 | Editorial(es): 2 | Categoría(s): 3 | Libro(s): 4 | Publicación(es): 4 | Relaciones libro-categoría: 6
```

---

## 5. Consultas en ambos sentidos (resultados reales)

### Sentido directo (forward)

```python
cien = Book.objects.get(isbn="9780307474728")
cien.author          # Gabriel García Márquez
cien.publisher       # Random House
cien.categories.all() # [Novela, Realismo mágico]
cien.publication     # Cien años de soledad (1ª ed.) | pages: 471
```

### Sentido inverso (reverse, con `related_name`)

```python
garcia.books.all()          # [Cien años de soledad, El amor en los tiempos del cólera]
Publisher.objects.get(name="Random House").books.all()
Category.objects.get(name="Novela").books.all()   # 3 libros
```

### Publication consultable desde ambos lados (OneToOne) ✅

```python
cien.publication.book            # Cien años de soledad  (reverse relacionado)
cien.publication.book.pk == cien.pk   # True (mismo registro)
cien.publication.book.title       # Cien años de soledad (roundtrip book → publication → book)
```

### Filtros

```python
Book.objects.filter(author__name__contains="Isabel")          # Inés del alma mía
Book.objects.filter(categories__name="Novela")                # 3 libros
Book.objects.filter(publisher__city="Lima")                   # 2 libros
Author.objects.filter(books__title__contains="amor")          # Gabriel García Márquez
```

### Modelo intermedio (through) con campo extra

```python
BookCategory.objects.get(book=cien, category=novela).is_primary   # True
BookCategory.objects.filter(book=cien).count()                    # 2
```

---

## 6. Eliminación CASCADE y PROTECT (resultados reales)

### CASCADE (Book.author → Author)

```python
tmp.delete()      # elimina al autor de prueba
# Author gone: True | Book gone: True  → el libro asociado se elimina automáticamente
```

### PROTECT (Book.publisher → Publisher)

```python
rh = Publisher.objects.get(name="Random House")
rh.delete()
# ProtectedError raised (Publisher referenced by Book.publisher).
# Publisher still exists: True
# Tras borrar sus libros, rh.delete() → OK
```

Con `on_delete=PROTECT` Django bloquea la eliminación de la editorial mientras tenga libros.

---

## 7. Detalle del libro: autor, categorías y editorial

- **URL lista:** http://127.0.0.1:8000/library/
- **URL detalle:** http://127.0.0.1:8000/library/book/1/

La vista `library.views.book_detail` usa `select_related("author", "publisher", "publication")` y `prefetch_related("categories")`, y el template `book_detail.html` muestra **Autor**, **Editorial**, **Categorías** y **Publicación** del libro.

---

## 8. Casos de prueba y resultados

Ejecución: `python manage.py test library` → **16 pruebas, 16 OK** (19 JSON de success).

| Caso | Resultado |
|------|-----------|
| `test_forward_book_author_and_publisher` | FK directo: `book.author` y `book.publisher` correctos |
| `test_forward_m2m_categories` | `book.categories` devuelve Novela y Realismo mágico |
| `test_forward_o2o_publication` | `book.publication` apunta a la publicación correcta |
| `test_reverse_author_books` | `author.books` (related_name) devuelve `[Cien años de soledad]` |
| `test_reverse_publisher_books` | `publisher.books` devuelve `[Inés del alma mía]` |
| `test_reverse_category_books` | `category.books` en Novela → 2 libros; Realismo mágico → 1 |
| `test_reverse_publication_book` | **Publication consultable desde ambos lados** (`publication.book`) |
| `test_filter_by_author_and_categories` | Filtros por `author__name`, `categories__name`, `publisher__city` |
| `test_filter_reverse_related_name` | Filtros inversos por `books__title` e `isbn` |
| `test_through_extra_field` | `BookCategory.is_primary` funciona; 2 relaciones por libro |
| `test_unique_book_category` | Restricción única (book, category) evita duplicados |
| `test_cascade_delete_author` | Borrar autor elimina sus libros (CASCADE) |
| `test_o2o_cascade_publication` | Borrar publicación elimina el libro (OneToOne CASCADE) |
| `test_protect_delete_publisher` | Borrar editorial con libros lanza `ProtectedError` |
| `test_book_detail_shows_relations` | Detalle muestra autor, editorial y categorías |
| `test_book_list_shows_books` | Lista muestra los libros |

Suite completa del proyecto: `python manage.py test` → **25 tests, 25 OK** (16 library + 9 rental). `manage.py check` → sin problemas.

---

## 9. Observaciones

- `Book.publication` es `OneToOneField`: solo puede existir una publicación por libro y un libro por publicación. Se debe crear la `Publication` **antes** que el `Book` porque el campo no admite `NULL` (error `NOT NULL constraint failed` si se invierte el orden).
- El modelo intermedio `BookCategory` permite agregar un campo extra (`is_primary`) que no sería posible con un ManyToMany simple.
- Con `PROTECT` el intento de borrar una editorial con libros lanza `ProtectedError`; con `CASCADE` el autor borrado arrastra a sus libros automáticamente.
- `related_name` por modelo permite consultas inversas legibles (ej. `author.books`, `publication.book`).
- Los archivos multimedia se sirven desde `/media/` en DEBUG gracias a Pillow + `MEDIA_ROOT`.

## 10. Conclusiones

Se implementaron las cinco relaciones de Django (ForeignKey, OneToOneField, ManyToManyField con `through`, y sus accesos inversos mediante `related_name`), se generaron las migraciones con su tabla intermedia, se cargaron los datos del enunciado (2 autores, 4 libros, 3 categorías, 2 editoriales) y se verificó —mediante consultas de doble sentido, filtros, borrado CASCADE/PROTECT y vistas— que el modelo funciona y que `Publication` se puede consultar desde ambos lados. Todo queda respaldado por 25 pruebas automáticas aprobadas y las evidencias recopiladas en este documento.