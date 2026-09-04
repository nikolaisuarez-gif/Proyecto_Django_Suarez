# Laboratorio 01 — Django

**Integrantes:**
- Ian Alexander Rau Reyes
- Nikolai Alexander Suarez Nuñez — nikolai.suarez@tecsup.edu.pe

**Repositorio:** https://github.com/nikolaisuarez-gif/Proyecto_Django_Suarez

Proyecto Django (Django 6.1) que contiene las aplicaciones `tasks`, `math_app` y la nueva app **`rental`** (Alquiler de Equipos).

---

## Ejercicio 1 — Problemática real

Una tienda local dedicada al **alquiler de equipos** (cámaras, laptops, proyectores, drones, consolas) lleva el control de su stock en papel. Esto genera demoras para saber qué equipos están disponibles, errores al registrar un alquiler y pérdida de información.

Se necesita una aplicación web que permita registrar los equipos, conocer su precio de alquiler diario y su estado de disponibilidad, de modo que el trabajador de la tienda pueda consultar y actualizar el catálogo de forma rápida y confiable.

**Usuarios:** el administrador o encargado de la tienda de alquiler de equipos.

---

## Ejercicio 2 — Requisitos funcionales

1. El sistema debe permitir **registrar un nuevo equipo** con nombre, categoría, precio de alquiler por día y stock.
2. El usuario debe poder **ver el listado de equipos registrados** con su estado de disponibilidad.
3. El sistema debe **mostrar el estado** de cada equipo (Disponible / Agotado) según su stock.
4. El usuario debe poder **consultar el precio de alquiler diario** de cada equipo.
5. El sistema debe **agregar un equipo nuevo al listado** después de validar el formulario de creación.

---

## Ejercicio 3 — Diseño del modelo de datos

**Entidad principal:** `Equipo`

| Campo       | Tipo de dato | Obligatorio | Justificación |
|-------------|--------------|-------------|----------------|
| `id`        | Entero (autoincremental) | Sí | Identifica de forma única cada equipo (Req. 1, 2). |
| `nombre`    | Texto (máx. 100) | Sí | Nombre del equipo que se va a alquilar (Req. 1, 2). |
| `categoria` | Texto (máx. 50) | Sí | Clasifica el equipo (cámaras, laptops, etc.) (Req. 1). |
| `precio_dia`| Decimal (S/) | Sí | Precio de alquiler por día (Req. 4). |
| `stock`     | Entero | Sí | Cantidad disponible; controla la disponibilidad (Req. 1, 3, 5). |
| `disponible`| Booleano | Sí | Estado (Disponible/Agotado) derivado del stock (Req. 3). |

---

## Ejercicio 4 — Nueva App

Se creó la aplicación **`rental`** dentro del proyecto `todoproject` y se registró en `INSTALLED_APPS` de `todoproject/settings.py`.

Estructura de la app:

```
rental/
├── models.py          # Datos estáticos (lista de diccionarios)
├── views.py           # equipo_list y equipo_create
├── forms.py           # EquipoForm (forms.Form, no ModelForm)
├── urls.py            # Rutas de la app (app_name = "rental")
├── tests.py           # Casos de prueba del flujo completo
└── templates/
    ├── base.html      # Plantilla base con Tailwind
    └── rental/
        ├── equipo_list.html
        └── equipo_form.html
```

---

## Ejercicio 5 — Model con datos estáticos

En `rental/models.py` los datos se definen como una **lista de diccionarios** `EQUIPOS` con 5 registros de ejemplo:

- Cámara Canon EOS R5 (Fotografía, S/ 50.00/día, stock 3)
- Laptop Dell XPS 15 (Informática, S/ 40.00/día, stock 2)
- Proyector Epson EB-2155W (Presentaciones, S/ 35.00/día, stock 4)
- Drone DJI Mini 3 (Drones, S/ 60.00/día, stock 1)
- Consola PlayStation 5 (Videojuegos, S/ 45.00/día, stock 0 → Agotado)

> ⚠️ No hay migraciones ni base de datos: esta lista es la única fuente de datos. Los registros agregados en memoria **se pierden al reiniciar el servidor** — esperado en este laboratorio.

---

## Ejercicio 6 — Listado (View + URL + Template)

- **View:** `views.equipo_list` recorre `EQUIPOS` y lo pasa al template.
- **URL:** `rental/` → `views.equipo_list` (registrada en `todoproject/urls.py` como `path('rental/', include('rental.urls'))`).
- **Template:** `equipo_list.html` **hereda de `base.html`** y muestra cada equipo en tarjetas con su estado.

```
Request → URL (/rental/) → View → Model (EQUIPOS) → Template (base.html + equipo_list.html) → Response
```

---

## Ejercicio 7 — Formulario (Forms)

`rental/forms.py` define `EquipoForm(forms.Form)` (no `ModelForm`, porque no hay modelo de base de datos) con los campos: `nombre`, `categoria`, `precio_dia` y `stock`, correspondientes a los requisitos del Ejercicio 2.

---

## Ejercicio 8 — Vista de creación

`views.equipo_create`:
1. En **GET** muestra el formulario.
2. En **POST** valida los datos con `form.is_valid()`.
3. Si es válido, **agrega el nuevo equipo** a `EQUIPOS` (con `id` autoincremental y `disponible` según el stock) y **redirige al listado**.
4. Si es inválido, vuelve a renderizar el formulario con los errores.

> Los datos agregados viven solo en memoria de proceso; al reiniciar el servidor se restablece `EQUIPOS` original.

---

## Ejercicio 9 — Verificación del flujo completo

Flujo probado de principio a fin con `manage.py runserver`:

1. `GET /rental/` → Listado con los 5 equipos estáticos.
2. `GET /rental/nuevo/` → Formulario "Registrar nuevo equipo".
3. `POST /rental/nuevo/` con datos válidos → **302** a `/rental/`.
4. `GET /rental/` → El nuevo equipo aparece en el listado (6 equipos).
5. `POST /rental/nuevo/` con datos inválidos → El formulario se re-renderiza mostrando errores.

**Recorrido MVT:**

```
Browser → Request (GET/POST /rental/..)
       → URLConf (todoproject/urls.py → rental/urls.py)
       → View (equipo_list | equipo_create)
       → Model (EQUIPOS, datos estáticos)
       → Template (base.html → equipo_list.html | equipo_form.html)
       → Response (HTML)
```

**Capturas del flujo funcionando** (carpeta `capturas/`):

1. `capturas/01_listado.png` — Listado inicial con los 5 equipos estáticos.
2. `capturas/02_formulario.png` — Formulario "Registrar nuevo equipo".
3. `capturas/03_listado_con_nuevo.png` — Listado después de crear "Cámara Sony A7 IV" (el nuevo registro se refleja; 6 equipos).

### Casos de prueba (`rental/tests.py`)

Ejecutar con: `python manage.py test rental`

| Caso | Resultado |
|------|-----------|
| `test_listado_responde_200_y_usa_el_template` | GET /rental/ → 200 y usa `equipo_list.html` |
| `test_listado_muestra_los_5_equipos_estaticos` | Muestra los 5 equipos estáticos, "Disponible" y "Agotado" |
| `test_listado_muestra_estado_por_stock` | `disponible` es True/False según el stock |
| `test_formulario_get_renderiza_el_template` | GET /rental/nuevo/ → 200 y usa `equipo_form.html` |
| `test_post_valido_redirige_y_agrega_registro` | POST válido → 302 y agrega el equipo a `EQUIPOS` |
| `test_listado_refleja_el_nuevo_registro` | El listado muestra el equipo recién creado |
| `test_post_invalido_no_agrega_y_muestra_errores` | POST inválido → 200 con errores, sin agregar |
| `test_form_valida_datos_correctos` | `EquipoForm` acepta datos válidos |
| `test_form_rechaza_stock_cero` | `EquipoForm` rechaza stock = 0 |

**Resultado:** 9 pruebas, 9 OK (`Ran 9 tests ... OK`).

**Convivencia con las demás apps:** la app `rental` es una app Django independiente que se conecta al mismo `Project` (`todoproject`). Cada app aporta sus propias rutas con prefijos (`/rental/`, `/math/`, `/`) y sus propios templates. El `Project` actúa como contenedor: `settings.INSTALLED_APPS` las registra y `todoproject/urls.py` las enruta, sin mezclar código entre apps. `rental` además introduce `base.html` (plantilla base con Tailwind) de la cual heredan sus templates de listado y formulario.

---

## Ejercicio 10 — Publicación en GitHub

- `requirements.txt`: `Django==6.1`.
- Estructura del proyecto:

```
Proyecto_Django_Suarez/
├── .gitignore
├── requirements.txt
├── README.md
├── capturas/              (capturas de pantalla del flujo)
├── documentos/
│   ├── ejercicio_1_2_requisitos.md      (Ej. 1 y 2)
│   ├── ejercicio_3_modelo_datos.md      (Ej. 3)
│   ├── evidencia_Ian_Rau_Reyes.md       (evidencia Integrante 1)
│   └── evidencia_Nikolai_Suarez_Nunez.md (evidencia Integrante 2)
└── todoproject/
    ├── manage.py
    ├── todoproject/         (settings, urls)
    ├── tasks/               (app base)
    ├── math_app/            (app base)
    └── rental/              (nueva app: Alquiler de Equipos)
```

## Cómo ejecutar

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
cd todoproject
python manage.py runserver
```

Luego abrir:

- Listado de equipos: http://127.0.0.1:8000/rental/
- Registrar equipo: http://127.0.0.1:8000/rental/nuevo/