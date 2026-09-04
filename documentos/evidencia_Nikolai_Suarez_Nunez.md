# Evidencia — Integrante 2

**Nombre:** Nikolai Alexander Suarez Nuñez
**Título:** App `rental` — Sistema de Alquiler de Equipos (Laboratorio Django)

---

## Capturas del flujo

1. **Listado inicial (5 equipos estáticos):** `capturas/01_listado.png`
2. **Formulario "Registrar nuevo equipo":** `capturas/02_formulario.png`
3. **Listado después de crear "Cámara Sony A7 IV" (6 equipos):** `capturas/03_listado_con_nuevo.png`

---

## Código (resumen de la app `rental`)

```python
# models.py — Datos estáticos (única fuente de datos, en memoria)
EQUIPOS = [
    {"id": 1, "nombre": "Cámara Canon EOS R5", "categoria": "Fotografía",
     "precio_dia": 50.0, "stock": 3, "disponible": True},
    {"id": 2, "nombre": "Laptop Dell XPS 15", "categoria": "Informática",
     "precio_dia": 40.0, "stock": 2, "disponible": True},
    {"id": 5, "nombre": "Consola PlayStation 5", "categoria": "Videojuegos",
     "precio_dia": 45.0, "stock": 0, "disponible": False},
]

# views.py — Listado y creación
def equipo_list(request):
    return render(request, "rental/equipo_list.html", {"equipos": EQUIPOS})

def equipo_create(request):
    if request.method == "POST":
        form = EquipoForm(request.POST)
        if form.is_valid():
            nuevo_id = max((e["id"] for e in EQUIPOS), default=0) + 1
            stock = form.cleaned_data["stock"]
            EQUIPOS.append({
                "id": nuevo_id,
                "nombre": form.cleaned_data["nombre"],
                "categoria": form.cleaned_data["categoria"],
                "precio_dia": float(form.cleaned_data["precio_dia"]),
                "stock": stock,
                "disponible": stock > 0,
            })
            return redirect("rental:equipo_list")
    else:
        form = EquipoForm()
    return render(request, "rental/equipo_form.html", {"form": form})

# forms.py — forms.Form (no ModelForm, no hay base de datos)
class EquipoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    categoria = forms.CharField(max_length=50)
    precio_dia = forms.DecimalField(min_value=0, max_digits=8, decimal_places=2)
    stock = forms.IntegerField(min_value=1)
```

---

## Explicación del flujo MVT aplicado

```
Browser → Request (GET/POST /rental/..)
        → URLConf (todoproject/urls.py → rental/urls.py)
        → View (equipo_list | equipo_create)
        → Model (EQUIPOS, datos estáticos)
        → Template (base.html → equipo_list.html | equipo_form.html)
        → Response (HTML)
```

La app `rental` convive con `core` dentro del mismo `Project` (`todoproject`). Cada app (tasks, math_app, rental) aporta sus propias rutas con prefijo (`/`, `/math/`, `/rental/`) y su propio template. El `Project` actúa como contenedor: `INSTALLED_APPS` las registra y `todoproject/urls.py` las enruta, sin mezclar código entre apps.

**Aporte del integrante a la evidencia:** definición de `models.py` (datos estáticos) y `forms.py` (validación), y verificación de que el nuevo registro se refleje en el listado tras el POST.

---

## Casos de prueba

Ejecutar con: `python manage.py test rental`

| Caso | Resultado |
|------|-----------|
| `test_formulario_get_renderiza_el_template` | GET /rental/nuevo/ → 200 y usa `equipo_form.html` |
| `test_listado_refleja_el_nuevo_registro` | El listado muestra el equipo recién creado |
| `test_form_valida_datos_correctos` | `EquipoForm` acepta datos válidos |
| `test_form_rechaza_stock_cero` | `EquipoForm` rechaza stock = 0 |

**Resultado:** 9 pruebas, 9 OK.
