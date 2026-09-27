from django.test import TestCase
from django.urls import reverse

from .forms import ChoiceFormSet, clean_choices
from .models import Choice, Exam, Question


class ExamModelTests(TestCase):
    def test_se_crea_un_examen(self):
        exam = Exam.objects.create(title="Examen 1", description="Practica")
        self.assertEqual(str(exam), "Examen 1")
        self.assertTrue(exam.active)

    def test_pregunta_pertenece_a_un_examen(self):
        exam = Exam.objects.create(title="Examen 1")
        question = Question.objects.create(exam=exam, text="Pregunta A")
        self.assertEqual(question.exam, exam)
        self.assertEqual(list(exam.questions.all()), [question])
        self.assertEqual(str(question), "Pregunta A")

    def test_opcion_pertenece_a_una_pregunta(self):
        exam = Exam.objects.create(title="Examen 1")
        question = Question.objects.create(exam=exam, text="Pregunta A")
        choice = Choice.objects.create(question=question, text="Opcion 1", is_correct=True)
        self.assertEqual(choice.question, question)
        self.assertEqual(list(question.choices.all()), [choice])
        self.assertEqual(str(choice), "Opcion 1")

    def test_cascade_borra_preguntas_y_opciones(self):
        exam = Exam.objects.create(title="Examen 1")
        question = Question.objects.create(exam=exam, text="Pregunta A")
        Choice.objects.create(question=question, text="Opcion 1", is_correct=True)
        exam.delete()
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Choice.objects.count(), 0)

    def test_meta_ordering_por_defecto(self):
        exam1 = Exam.objects.create(title="B")
        exam2 = Exam.objects.create(title="A")
        self.assertEqual(Exam._meta.ordering, ["-created_at", "id"])
        self.assertEqual(Question._meta.ordering, ["id"])


class SeedDataTests(TestCase):
    def test_examen_con_dos_preguntas_y_cuatro_opciones(self):
        from django.core.management import call_command

        call_command("seed_exams", verbosity=0)
        self.assertEqual(Exam.objects.count(), 1)
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(Choice.objects.count(), 8)
        for question in Question.objects.all():
            self.assertEqual(question.choices.count(), 4)
            self.assertEqual(question.choices.filter(is_correct=True).count(), 1)


class FormsetValidationTests(TestCase):
    def setUp(self):
        self.exam = Exam.objects.create(title="Examen 1")
        self.question = Question.objects.create(exam=self.exam, text="Pregunta A")

    def post(self, correctas):
        data = {
            "choices-TOTAL_FORMS": "3",
            "choices-INITIAL_FORMS": "0",
            "choices-MIN_NUM_FORMS": "2",
            "choices-MAX_NUM_FORMS": "1000",
            "choices-0-text": "Opcion A",
            "choices-1-text": "Opcion B",
            "choices-2-text": "Opcion C",
        }
        for i in correctas:
            data[f"choices-{i}-is_correct"] = "on"
        return data

    def test_una_sola_correcta_es_valido(self):
        formset = ChoiceFormSet(self.post([0]), instance=self.question)
        self.assertTrue(formset.is_valid())
        _, error = clean_choices(formset)
        self.assertIsNone(error)

    def test_dos_correctas_da_error(self):
        formset = ChoiceFormSet(self.post([0, 1]), instance=self.question)
        self.assertTrue(formset.is_valid())
        _, error = clean_choices(formset)
        self.assertEqual(error, "Solo puede existir UNA opcion correcta por pregunta.")

    def test_ninguna_correcta_da_error(self):
        formset = ChoiceFormSet(self.post([]), instance=self.question)
        self.assertTrue(formset.is_valid())
        _, error = clean_choices(formset)
        self.assertEqual(error, "Debe existir al menos una opcion correcta.")


class ViewTests(TestCase):
    def setUp(self):
        self.exam = Exam.objects.create(title="Examen 1", description="Practica")
        self.question = Question.objects.create(exam=self.exam, text="Pregunta A")
        self.choice = Choice.objects.create(
            question=self.question, text="Opcion 1", is_correct=True
        )

    def test_listado_responde_200(self):
        r = self.client.get(reverse("exams:exam_list"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "exams/exam_list.html")

    def test_detalle_responde_200(self):
        r = self.client.get(reverse("exams:exam_detail", args=[self.exam.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Pregunta A")

    def test_detalle_pregunta_responde_200(self):
        r = self.client.get(reverse("exams:question_detail", args=[self.question.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Opcion 1")

    def test_crear_examen_get(self):
        r = self.client.get(reverse("exams:exam_create"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "exams/exam_form.html")

    def test_crear_examen_post_valido(self):
        Exam.objects.all().delete()
        data = {
            "title": "Examen nuevo",
            "description": "Prueba",
            "active": "on",
            "text": "Pregunta nueva",
            "choices-TOTAL_FORMS": "3",
            "choices-INITIAL_FORMS": "0",
            "choices-MIN_NUM_FORMS": "2",
            "choices-MAX_NUM_FORMS": "1000",
            "choices-0-text": "A",
            "choices-0-is_correct": "on",
            "choices-1-text": "B",
            "choices-2-text": "C",
        }
        r = self.client.post(reverse("exams:exam_create"), data)
        exam = Exam.objects.get(title="Examen nuevo")
        self.assertRedirects(r, reverse("exams:exam_detail", args=[exam.pk]))
        self.assertEqual(exam.questions.count(), 1)
        self.assertEqual(exam.questions.first().choices.count(), 3)
        self.assertEqual(exam.questions.first().choices.filter(is_correct=True).count(), 1)

    def test_crear_examen_post_con_dos_correctas_no_guarda(self):
        Exam.objects.all().delete()
        data = {
            "title": "Examen malo",
            "description": "",
            "text": "Pregunta mala",
            "choices-TOTAL_FORMS": "3",
            "choices-INITIAL_FORMS": "0",
            "choices-MIN_NUM_FORMS": "2",
            "choices-MAX_NUM_FORMS": "1000",
            "choices-0-text": "A",
            "choices-0-is_correct": "on",
            "choices-1-text": "B",
            "choices-1-is_correct": "on",
            "choices-2-text": "C",
        }
        r = self.client.post(reverse("exams:exam_create"), data)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Solo puede existir UNA opcion correcta")
        self.assertFalse(Exam.objects.filter(title="Examen malo").exists())

    def test_agregar_pregunta_post_valido(self):
        data = {
            "text": "Segunda pregunta",
            "choices-TOTAL_FORMS": "2",
            "choices-INITIAL_FORMS": "0",
            "choices-MIN_NUM_FORMS": "2",
            "choices-MAX_NUM_FORMS": "1000",
            "choices-0-text": "X",
            "choices-0-is_correct": "on",
            "choices-1-text": "Y",
        }
        r = self.client.post(
            reverse("exams:question_add", args=[self.exam.pk]), data
        )
        self.assertRedirects(r, reverse("exams:exam_detail", args=[self.exam.pk]))
        self.assertEqual(self.exam.questions.count(), 2)


class AdminTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        User.objects.create_superuser(
            username="nikolai", email="nikolai.suarez@tecsup.edu.pe", password="Nikolai2026*"
        )

    def test_registrados_en_el_admin(self):
        from django.contrib import admin

        for model in (Exam, Question, Choice):
            self.assertIn(model, admin.site._registry)

    def test_admin_responde_200(self):
        self.client.login(username="nikolai", password="Nikolai2026*")
        for url in ("/admin/", "/admin/exams/exam/", "/admin/exams/question/", "/admin/exams/choice/"):
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200, url)
