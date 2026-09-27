from django.db import models


class Exam(models.Model):
    """Examen: entidad principal. Agrupa las preguntas de una evaluacion."""

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
    """Pregunta que pertenece a un examen (relacion 1 a N con Exam)."""

    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.CharField(max_length=300)
    puntaje = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["id"]
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"

    def __str__(self):
        return self.text


class Choice(models.Model):
    """Opcion de respuesta que pertenece a una pregunta (relacion 1 a N)."""

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        verbose_name = "Opcion"
        verbose_name_plural = "Opciones"

    def __str__(self):
        return self.text
