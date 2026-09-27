# Laboratorio — Creación de Modelos en Django (App `exams`)

**Estudiante:** Nikolai Alexander Suarez Nuñez
**Repositorio:** https://github.com/nikolaisuarez-gif/Proyecto_Django_Suarez
**App:** `exams` (dentro del proyecto `todoproject`) — Django 6.1

---

## 1. Modelos (`exams/models.py`)

Tres modelos con una relación **1 a N** en cascada:

```
Exam (1) ────< Question (1) ────< Choice
```

```python
class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "id"]
        verbose_name = "Examen"
        verbose_name_plural = "Examenes"

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=300)
    puntaje = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["id"]
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        verbose_name = "Opción"
        verbose_name_plural = "Opciones"

    def __str__(self):
        return self.text
```

### 1.1 Relaciones

| Campo | Tipo | `on_delete` | `related_name` |
|-------|------|-------------|----------------|
| `Question.exam` → `Exam` | `ForeignKey` | `CASCADE` | `questions` |
| `Choice.question` → `Question` | `ForeignKey` | `CASCADE` | `choices` |

`CASCADE` porque si se borra un examen tiene que disappear todo su contenido (preguntas y opciones). `related_name` permite escribir `exam.questions.all()` y `question.choices.all()` en vez de `exam.question_set.all()`.

### 1.2 `__str__`

Sin `__str__`, el admin y el shell mostrarían `Exam object (1)`. Con `__str__` se muestra `Examen de Django - Modelos`, que es lo que se ve en las capturas del admin.

### 1.3 `Meta`

- `ordering`: define el orden por defecto de los `QuerySet`, sin usar `order_by` en cada consulta.
- `verbose_name` / `verbose_name_plural`: nombres en singular y plural que se muestran en el admin.

---

## 2. Migraciones y base de datos

```bash
python manage.py makemigrations exams
python manage.py migrate
python manage.py showmigrations exams
```

Salida de `makemigrations` (1era vez):

```
Migrations for 'exams':
  exams\migrations\0001_initial.py
    + Create model Exam
    + Create model Question
    + Create model Choice
```

Comprobación de la base de datos (`db.sqlite3`) con `PRAGMA table_info`:

```
== exams_exam
    (0, 'id', 'INTEGER', 1, None, 1)
    (1, 'title', 'varchar(200)', 1, None, 0)
    (2, 'description', 'TEXT', 1, None, 0)
    (3, 'active', 'bool', 1, None, 0)
    (4, 'created_at', 'datetime', 1, None, 0)

== exams_question
    (0, 'id', 'INTEGER', 1, None, 1)
    (1, 'text', 'varchar(300)', 1, None, 0)
    (2, 'exam_id', 'bigint', 1, None, 0)
    (3, 'puntaje', 'integer unsigned', 1, None, 0)

== exams_choice
    (0, 'id', 'INTEGER', 1, None, 1)
    (1, 'text', 'varchar(200)', 1, None, 0)
    (2, 'is_correct', 'bool', 1, None, 0)
    (3, 'question_id', 'bigint', 1, None, 0)
```

Django creó las claves foráneas `exam_id` y `question_id` de tipo `bigint`.

Evidencias: `documentos/evidencias_lab06/01_migraciones.txt`, `03_base_datos.txt`.

---

## 3. Formularios y formset de opciones (`exams/forms.py`)

- `ExamForm(forms.ModelForm)` → `title`, `description`, `active`.
- `QuestionForm(forms.ModelForm)` → `text`.
- `ChoiceForm(forms.ModelForm)` → `text`, `is_correct`.
- `ChoiceFormSet` con `inlineformset_factory(Question, Choice, extra=3, min_num=2, can_delete=True)`.

El formset permite escribir varias opciones en un solo formulario. `extra=3` muestra 3 filas vacías y `min_num=2` obliga a tener al menos 2 opciones.

### 3.1 Validación de una sola respuesta correcta

```python
def clean_choices(formset):
    if not formset.is_valid():
        return formset, "Revisa los datos de las opciones."

    correctas = 0
    for form in formset.forms:
        if not form.cleaned_data or form.cleaned_data.get("DELETE"):
            continue
        if form.cleaned_data.get("is_correct"):
            correctas += 1

    if correctas == 0:
        return formset, "Debe existir al menos una opción correcta."
    if correctas > 1:
        return formset, "Solo puede existir UNA opción correcta por pregunta."

    return formset, None
```

Cuenta las casillas marcadas y avisa si hay 0 o más de 1. El error se muestra en el template.

Evidencia: `capturas/lab06_11_validacion_dos_correctas.png` y `lab06_12_validacion_ninguna_correcta.png`.

---

## 4. Vistas, URLs y plantillas

**`exams/urls.py`**

```python
app_name = "exams"
urlpatterns = [
    path("", views.exam_list, name="exam_list"),
    path("nuevo/", views.exam_create, name="exam_create"),
    path("<int:pk>/", views.exam_detail, name="exam_detail"),
    path("<int:pk>/pregunta/nueva/", views.question_add, name="question_add"),
    path("pregunta/<int:pk>/", views.question_detail, name="question_detail"),
]
```

Registrado en `todoproject/urls.py` con `path('exams/', include('exams.urls'))` y en `INSTALLED_APPS` con `'exams'`.

| URL | Vista | Qué hace |
|-----|-------|----------|
| `/exams/` | `exam_list` | Lista los exámenes con su número de preguntas |
| `/exams/nuevo/` | `exam_create` | Crea un examen con una pregunta y sus opciones |
| `/exams/1/` | `exam_detail` | Muestra el examen con preguntas y opciones |
| `/exams/1/pregunta/nueva/` | `question_add` | Agrega otra pregunta al examen |
| `/exams/pregunta/1/` | `question_detail` | Muestra una pregunta con sus opciones |

**Plantillas** (`exams/templates/exams/`): `base.html`, `exam_list.html`, `exam_detail.html`, `exam_form.html`, `question_form.html`, `question_detail.html`. Todas heredan de `base.html` y usan Tailwind por CDN, igual que las demás apps del proyecto.

Flujo: `Request → URL → View → Model → Template → Response`.

---

## 5. Django Admin y superusuario

```bash
python manage.py createsuperuser   # usuario: nikolai
```

- **Superusuario:** `nikolai` (Nikolai Alexander Suarez Nuñez).
- `ExamAdmin` con `QuestionInline` (preguntas dentro del examen).
- `QuestionAdmin` con `ChoiceInline` (opciones dentro de la pregunta).
- `ChoiceAdmin` con filtro por `is_correct` y por `question__exam`.

Con los inlines se puede armar todo el examen desde una sola pantalla del admin.

Evidencia: `capturas/lab06_01_admin_home.png` a `lab06_05_admin_opciones.png`.

---

## 6. Datos creados

Comando `python manage.py seed_exams` (app `exams/management/commands/seed_exams.py`):

```
Examen(es): 1 | Pregunta(s): 2 | Opcion(es): 8
```

**1 examen, 2 preguntas, 4 opciones cada una** (2 × 4 = 8):

| # | Pregunta | Opciones | Correcta |
|---|----------|----------|----------|
| 1 | ¿Qué comando genera las migraciones de un app? | `makemigrations`, `migrate`, `runserver`, `createsuperuser` | `makemigrations` |
| 2 | ¿Qué método define el texto que se muestra en el admin? | `def Meta()`, `def __str__()`, `def save()`, `def get_absolute_url()` | `def __str__()` |

---

## 7. Campo `puntaje` en `Question` y su migración

Se agregó el campo después de tener el examen funcionando:

```python
puntaje = models.PositiveIntegerField(default=1)
```

```bash
python manage.py makemigrations exams
```

```
Migrations for 'exams':
  exams\migrations\0002_question_puntaje.py
    + Add field puntaje to question
```

```bash
python manage.py migrate
```

```
Applying exams.0002_question_puntaje... OK
```

Django lo agregó como `integer unsigned` (por `PositiveIntegerField`) y las 2 preguntas existentes quedaron con `puntaje = 1` gracias al `default=1`.

Evidencia: `capturas/lab06_07_web_detalle_puntaje.png` y `lab06_10_web_detalle_pregunta_puntaje.png`.

---

## 8. Justificación de los campos

| Modelo | Campo | Tipo Django | Por qué ese tipo |
|--------|-------|-------------|------------------|
| `Exam` | `id` | `AutoField` (automático) | Identifica cada examen de forma única |
| `Exam` | `title` | `CharField(200)` | Es un texto corto; 200 alcanza para un título y SQLite no limita como otros motores |
| `Exam` | `description` | `TextField(blank=True)` | Texto largo opcional para describir de qué trata el examen |
| `Exam` | `active` | `BooleanField(default=True)` | Permite ocultar un examen terminado sin borrarlo de la base de datos |
| `Exam` | `created_at` | `DateTimeField(auto_now_add=True)` | Guarda la fecha de creación sola, sirve para ordenar con `Meta.ordering` |
| `Question` | `exam` | `ForeignKey(CASCADE)` | Una pregunta siempre pertenece a un examen; si se borra el examen, se borran sus preguntas |
| `Question` | `text` | `CharField(300)` | El enunciado es un texto de una línea y 300 caracteres bastan |
| `Question` | `puntaje` | `PositiveIntegerField(default=1)` | Los puntos no pueden ser negativos y `default=1` rellena las preguntas ya creadas |
| `Choice` | `question` | `ForeignKey(CASCADE)` | Una opción siempre pertenece a una pregunta |
| `Choice` | `text` | `CharField(200)` | Una opción es un texto corto |
| `Choice` | `is_correct` | `BooleanField(default=False)` | Marca la respuesta correcta; por defecto ninguna lo es, así se elige a propósito |

Todos los `CharField` llevan `max_length` porque Django lo necesita para definir la columna `varchar(n)` en la base de datos.

---

## 9. Casos de prueba

```bash
python manage.py test exams
```

**Resultado: `Ran 18 tests ... OK`**

| Caso | Qué comprueba |
|------|---------------|
| `test_se_crea_un_examen` | Se crea un examen, `__str__` devuelve el título y `active` es `True` |
| `test_pregunta_pertenece_a_un_examen` | La pregunta apunta a su examen y aparece en `exam.questions.all()` |
| `test_opcion_pertenece_a_una_pregunta` | La opción apunta a su pregunta y aparece en `question.choices.all()` |
| `test_cascade_borra_preguntas_y_opciones` | Al borrar el examen se borran también preguntas y opciones |
| `test_meta_ordering_por_defecto` | `Meta.ordering` es `["-created_at","id"]` en Exam y `["id"]` en Question |
| `test_examen_con_dos_preguntas_y_cuatro_opciones` | El seed crea 1 examen, 2 preguntas, 8 opciones y 1 correcta por pregunta |
| `test_una_sola_correcta_es_valido` | Con 1 marcada el formset es válido y `clean_choices` no da error |
| `test_dos_correctas_da_error` | Con 2 marcadas aparece "Solo puede existir UNA opción correcta por pregunta." |
| `test_ninguna_correcta_da_error` | Con 0 marcadas aparece "Debe existir al menos una opción correcta." |
| `test_listado_responde_200` | `GET /exams/` → 200 y usa `exam_list.html` |
| `test_detalle_responde_200` | `GET /exams/1/` → 200 y muestra la pregunta |
| `test_detalle_pregunta_responde_200` | `GET /exams/pregunta/1/` → 200 y muestra la opción |
| `test_crear_examen_get` | `GET /exams/nuevo/` → 200 y usa `exam_form.html` |
| `test_crear_examen_post_valido` | POST válido → 302 y guarda examen, pregunta y 3 opciones con 1 correcta |
| `test_crear_examen_post_con_dos_correctas_no_guarda` | POST con 2 correctas → 200 con error y **no** guarda nada |
| `test_agregar_pregunta_post_valido` | POST en `/exams/1/pregunta/nueva/` → 302 y el examen queda con 2 preguntas |
| `test_registrados_en_el_admin` | `Exam`, `Question` y `Choice` están en `admin.site._registry` |
| `test_admin_responde_200` | El admin responde 200 en las 4 páginas de los 3 modelos |

Evidencia: `documentos/evidencias_lab06/02_pruebas.txt`.

---

## 10. Observaciones de las migraciones

1. `makemigrations` **no crea** la tabla, solo escribe el archivo `.py` con los cambios. `migrate` es el que las crea de verdad en la base de datos. Son dos pasos distintos.
2. La primera migración se llama `0001_initial.py` y Django la detectó automáticamente; no hubo que escribirla a mano.
3. Al agregar `puntaje` se generó la `0002_question_puntaje.py` en vez de modificar la `0001`. Eso es correcto: las migraciones ya aplicadas no se tocan, porque otros ambientes ya tienen esa versión.
4. Como `puntaje` tiene `default=1`, la migración funcionó sin pedir datos: las 2 preguntas que ya existían pasaron a `puntaje = 1` automáticamente. Si no tuviera `default`, Django habría pedido escribir un valor.
5. `PositiveIntegerField` terminó como `integer unsigned`, que en SQLite impide guardar negativos.
6. `showmigrations exams` muestra `[X] 0001_initial` y `[X] 0002_question_puntaje`, las dos aplicadas.
7. Las claves foráneas quedaron como columnas `bigint` (`exam_id`, `question_id`) con un índice creado automáticamente por Django.

---

## 11. Conclusiones

1. Antes de este laboratorio yo usaba Django solo con datos fijos en el código, sin base de datos. Ver que un modelo se convierte solo en una tabla de verdad me aclaró mucho las cosas: el `models.py` es el código y la tabla es el resultado. Lo mejor fue ver que borrar un examen con `CASCADE` también desaparece con todas sus preguntas y opciones, o sea que la base de datos mantiene la consistencia sola y yo no tengo que acordarme de borrar a mano.

2. Lo que más me costó fue el formset de opciones, porque el `management_form` con esos campos escondidos (`choices-TOTAL_FORMS`, etc.) parece un bloque de código raro. Cuando entendí que el navegador manda varias filas del mismo formulario y el prefijo `choices-` las separa, ya se entendió. También me confundí al principio con el `__str__`, porque no entendía para qué servía si el admin de todas formas funcionaba; hasta que vi en las capturas que sin ese método salía `Question object (1)` en vez del texto real.

3. La parte que más me gustó fue agregar el campo `puntaje` porque me mostró que las migraciones son como un historial del proyecto. La primera vez que corrí `makemigrations` ya no se puede modificar la `0001` y por eso se creó la `0002`; eso me enseñó a pensar que el orden importa y que conviene hacer los cambios chicos y probarlos uno por uno. Al final, con los 18 tests pasando, la base de datos migrada, el admin con sus inlines y las páginas web, siento que ya entendí cómo encaja el MVT con la base de datos y no solo con datos estáticos.

---

## 12. Estructura y evidencias

```
Proyecto_Django_Suarez/
├── capturas/
│   ├── lab06_01_admin_home.png                    Admin (home, superusuario)
│   ├── lab06_02_admin_examenes.png                Admin: lista de exámenes
│   ├── lab06_03_admin_examen_inline.png           Admin: examen + preguntas inline
│   ├── lab06_04_admin_pregunta_inline.png         Admin: pregunta + opciones inline
│   ├── lab06_05_admin_opciones.png                Admin: lista de opciones
│   ├── lab06_06_web_listado.png                   Web: /exams/
│   ├── lab06_07_web_detalle.png                   Web: /exams/1/
│   ├── lab06_08_web_formulario_formset.png        Web: formulario con formset
│   ├── lab06_09_web_agregar_pregunta.png          Web: agregar pregunta
│   ├── lab06_10_web_detalle_pregunta.png          Web: detalle de pregunta
│   ├── lab06_11_validacion_dos_correctas.png      Error: 2 opciones correctas
│   ├── lab06_12_validacion_ninguna_correcta.png   Error: 0 opciones correctas
│   ├── lab06_07_web_detalle_puntaje.png           Web: detalle con campo puntaje
│   └── lab06_10_web_detalle_pregunta_puntaje.png  Web: pregunta con campo puntaje
├── documentos/
│   ├── evidencia_lab06_modelos.md                 (este documento)
│   └── evidencias_lab06/
│       ├── 01_migraciones.txt
│       ├── 02_pruebas.txt
│       └── 03_base_datos.txt
└── todoproject/
    ├── manage.py
    ├── todoproject/{settings.py, urls.py}         (exams registrada)
    └── exams/
        ├── models.py                              Exam, Question, Choice
        ├── forms.py                               ModelForms + ChoiceFormSet + clean_choices
        ├── views.py                               5 vistas
        ├── urls.py                                app_name = "exams"
        ├── admin.py                               3 ModelAdmin + 2 Inline
        ├── tests.py                               18 casos de prueba
        ├── management/commands/seed_exams.py      1 examen, 2 preguntas, 8 opciones
        ├── migrations/
        │   ├── 0001_initial.py
        │   └── 0002_question_puntaje.py
        └── templates/exams/                       base + 5 plantillas
```

### Comandos para reproducir

```bash
cd todoproject
python manage.py makemigrations exams
python manage.py migrate
python manage.py seed_exams
python manage.py createsuperuser
python manage.py test exams
python manage.py runserver
```

- `/exams/` — listado de exámenes
- `/exams/nuevo/` — crear examen con formset
- `/admin/` — Django Admin
