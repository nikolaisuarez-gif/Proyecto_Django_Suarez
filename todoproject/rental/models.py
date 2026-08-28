# Datos estáticos: esta lista es la única fuente de datos de la aplicación.
# No se usan migraciones ni base de datos. Al reiniciar el servidor, los
# registros agregados en memoria se pierden (comportamiento esperado).

EQUIPOS = [
    {
        "id": 1,
        "nombre": "Cámara Canon EOS R5",
        "categoria": "Fotografía",
        "precio_dia": 50.0,
        "stock": 3,
        "disponible": True,
    },
    {
        "id": 2,
        "nombre": "Laptop Dell XPS 15",
        "categoria": "Informática",
        "precio_dia": 40.0,
        "stock": 2,
        "disponible": True,
    },
    {
        "id": 3,
        "nombre": "Proyector Epson EB-2155W",
        "categoria": "Presentaciones",
        "precio_dia": 35.0,
        "stock": 4,
        "disponible": True,
    },
    {
        "id": 4,
        "nombre": "Drone DJI Mini 3",
        "categoria": "Drones",
        "precio_dia": 60.0,
        "stock": 1,
        "disponible": True,
    },
    {
        "id": 5,
        "nombre": "Consola PlayStation 5",
        "categoria": "Videojuegos",
        "precio_dia": 45.0,
        "stock": 0,
        "disponible": False,
    },
]