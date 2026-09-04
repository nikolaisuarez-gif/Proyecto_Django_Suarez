# Ejercicio 1 y 2 — Problemática real y Requisitos funcionales

**Integrantes:** Ian Alexander Rau Reyes · Nikolai Alexander Suarez Nuñez
**Proyecto:** DjangoInicial (config/core) — App: `rental` (Alquiler de Equipos)

---

## Ejercicio 1 — Investigar una problemática real

Una tienda local dedicada al **alquiler de equipos** (cámaras, laptops, proyectores, drones, consolas) lleva el control de su stock en papel. Esto genera demoras para saber qué equipos están disponibles, errores al registrar un alquiler y pérdida de información.

Se necesita una aplicación web que permita registrar los equipos, conocer su precio de alquiler diario y su estado de disponibilidad, de modo que el trabajador de la tienda pueda consultar y actualizar el catálogo de forma rápida y confiable.

**Usuarios:** el administrador o encargado de la tienda de alquiler de equipos.

---

## Ejercicio 2 — Capturar los requisitos

1. El sistema debe permitir **registrar un nuevo equipo** con nombre, categoría, precio de alquiler por día y stock.
2. El usuario debe poder **ver el listado de equipos registrados** con su estado de disponibilidad.
3. El sistema debe **mostrar el estado** de cada equipo (Disponible / Agotado) según su stock.
4. El usuario debe poder **consultar el precio de alquiler diario** de cada equipo.
5. El sistema debe **agregar un equipo nuevo al listado** después de validar el formulario de creación.
