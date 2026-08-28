from django.shortcuts import render, redirect

from .forms import EquipoForm
from .models import EQUIPOS


def equipo_list(request):
    """Muestra el listado de equipos disponibles (README: Request -> View -> Model)."""
    return render(request, "rental/equipo_list.html", {"equipos": EQUIPOS})


def equipo_create(request):
    """Muestra el formulario, valida el POST y agrega el equipo a la lista en memoria."""
    if request.method == "POST":
        form = EquipoForm(request.POST)
        if form.is_valid():
            nuevo_id = max((equipo["id"] for equipo in EQUIPOS), default=0) + 1
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