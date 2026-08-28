import copy

from django.test import TestCase
from django.urls import reverse

from .forms import EquipoForm
from .models import EQUIPOS


class RentalBaseTestCase(TestCase):
    """Restaura los datos estáticos entre pruebas (la lista es la única fuente de datos)."""

    def setUp(self):
        self.original = copy.deepcopy(EQUIPOS)

    def tearDown(self):
        EQUIPOS.clear()
        EQUIPOS.extend(self.original)


class EquipoListTests(RentalBaseTestCase):
    """Casos de prueba del listado de equipos."""

    def test_listado_responde_200_y_usa_el_template(self):
        response = self.client.get(reverse("rental:equipo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "rental/equipo_list.html")

    def test_listado_muestra_los_5_equipos_estaticos(self):
        response = self.client.get(reverse("rental:equipo_list"))
        self.assertEqual(len(EQUIPOS), 5)
        self.assertContains(response, "Canon EOS R5")
        self.assertContains(response, "PlayStation 5")
        self.assertContains(response, "Disponible")
        self.assertContains(response, "Agotado")

    def test_listado_muestra_estado_por_stock(self):
        self.assertTrue(EQUIPOS[0]["disponible"])
        self.assertFalse(EQUIPOS[-1]["disponible"])


class EquipoCreateTests(RentalBaseTestCase):
    """Casos de prueba del formulario y la creación de equipos."""

    def test_formulario_get_renderiza_el_template(self):
        response = self.client.get(reverse("rental:equipo_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "rental/equipo_form.html")
        self.assertIsInstance(response.context["form"], EquipoForm)

    def test_post_valido_redirige_y_agrega_registro(self):
        total_inicial = len(EQUIPOS)
        response = self.client.post(reverse("rental:equipo_create"), {
            "nombre": "Cámara Sony A7 IV",
            "categoria": "Fotografía",
            "precio_dia": "55.50",
            "stock": "2",
        })
        self.assertRedirects(response, reverse("rental:equipo_list"))
        self.assertEqual(len(EQUIPOS), total_inicial + 1)
        nuevo = EQUIPOS[-1]
        self.assertEqual(nuevo["nombre"], "Cámara Sony A7 IV")
        self.assertEqual(nuevo["precio_dia"], 55.5)
        self.assertTrue(nuevo["disponible"])

    def test_listado_refleja_el_nuevo_registro(self):
        before = len(EQUIPOS)
        response = self.client.post(reverse("rental:equipo_create"), {
            "nombre": "Cámara Sony A7 IV",
            "categoria": "Fotografía",
            "precio_dia": "55.50",
            "stock": "2",
        })
        self.assertRedirects(response, reverse("rental:equipo_list"))
        response = self.client.get(reverse("rental:equipo_list"))
        self.assertContains(response, "Cámara Sony A7 IV")
        self.assertEqual(len(EQUIPOS), before + 1)

    def test_post_invalido_no_agrega_y_muestra_errores(self):
        total_inicial = len(EQUIPOS)
        response = self.client.post(reverse("rental:equipo_create"), {
            "nombre": "",
            "categoria": "X",
            "precio_dia": "-5",
            "stock": "abc",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(EQUIPOS), total_inicial)
        self.assertContains(response, "Corrige los siguientes errores")


class EquipoFormTests(TestCase):
    """Casos de prueba de la validación del formulario."""

    def test_form_valida_datos_correctos(self):
        form = EquipoForm({
            "nombre": "Drone DJI Mini 4",
            "categoria": "Drones",
            "precio_dia": "70.00",
            "stock": "1",
        })
        self.assertTrue(form.is_valid())

    def test_form_rechaza_stock_cero(self):
        form = EquipoForm({
            "nombre": "Drone DJI Mini 4",
            "categoria": "Drones",
            "precio_dia": "70.00",
            "stock": "0",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("stock", form.errors)