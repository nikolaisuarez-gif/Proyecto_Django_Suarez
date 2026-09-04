# Ejercicio 3 — Diseño del modelo de datos

**Integrantes:** Ian Alexander Rau Reyes · Nikolai Alexander Suarez Nuñez
**App:** `rental` (Alquiler de Equipos)

---

**Entidad principal:** `Equipo`

| Campo | Tipo de dato | Obligatorio | Justificación |
|-------|--------------|:-----------:|---------------|
| `id` | Entero (autoincremental) | Sí | Identifica de forma única cada equipo (Req. 1, 2). |
| `nombre` | Texto (máx. 100) | Sí | Nombre del equipo que se va a alquilar (Req. 1, 2). |
| `categoria` | Texto (máx. 50) | Sí | Clasifica el equipo (cámaras, laptops, etc.) (Req. 1). |
| `precio_dia` | Decimal (S/) | Sí | Precio de alquiler por día (Req. 4). |
| `stock` | Entero | Sí | Cantidad disponible; controla la disponibilidad (Req. 1, 3, 5). |
| `disponible` | Booleano | Sí | Estado (Disponible/Agotado) derivado del stock (Req. 3). |

---

## Justificación según los requisitos

- **`id`**: necesario para identificar de forma única cada equipo y distinguir registros al mostrarlos en el listado (Req. 2) y al registrar nuevos (Req. 1, 5).
- **`nombre`**: es el dato principal que el usuario necesita visualizar para saber qué equipo se alquila (Req. 1, 2).
- **`categoria`**: permite clasificar los equipos, usada como filtro organizativo al registrar (Req. 1) y mostrar (Req. 2).
- **`precio_dia`**: requisito explícito del sistema para consultar el precio de alquiler por día (Req. 4).
- **`stock`**: determina la cantidad disponible y, junto con `disponible`, controla si un equipo se puede alquilar (Req. 1, 3, 5).
- **`disponible`**: se deriva del stock (`stock > 0`) y permite mostrar el estado Disponible/Agotado en el listado (Req. 3).

---

## Nota

No se usa base de datos: estos campos se representan como **lista de diccionarios** en `rental/models.py` (dato estático en memoria). No hay migraciones ni panel de administración (dentro del alcance del laboratorio).
