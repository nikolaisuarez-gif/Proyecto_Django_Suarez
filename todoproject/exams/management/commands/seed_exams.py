from django.core.management.base import BaseCommand

from exams.models import Choice, Exam, Question


class Command(BaseCommand):
    help = "Seed: 1 examen con 2 preguntas y 4 opciones cada una."

    def handle(self, *args, **options):
        exam, _ = Exam.objects.get_or_create(
            title="Examen de Django - Modelos",
            defaults={
                "description": "Examen de práctica con 2 preguntas sobre modelos de Django.",
                "active": True,
            },
        )

        datos = [
            {
                "text": "¿Qué comando genera las migraciones de un app?",
                "opciones": [
                    ("python manage.py makemigrations", True),
                    ("python manage.py migrate", False),
                    ("python manage.py runserver", False),
                    ("python manage.py createsuperuser", False),
                ],
            },
            {
                "text": "¿Qué método define el texto que se muestra en el admin?",
                "opciones": [
                    ("def Meta()", False),
                    ("def __str__()", True),
                    ("def save()", False),
                    ("def get_absolute_url()", False),
                ],
            },
        ]

        for item in datos:
            question, _ = Question.objects.get_or_create(
                exam=exam, text=item["text"]
            )
            for texto, correcta in item["opciones"]:
                Choice.objects.get_or_create(
                    question=question,
                    text=texto,
                    defaults={"is_correct": correcta},
                )

        self.stdout.write(self.style.SUCCESS(
            f"Examen(es): {Exam.objects.count()} | Pregunta(s): {Question.objects.count()} "
            f"| Opcion(es): {Choice.objects.count()}"
        ))
