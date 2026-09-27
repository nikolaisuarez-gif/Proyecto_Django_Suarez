from django.contrib import admin

from .models import Choice, Exam, Question


class ChoiceInline(admin.TabularInline):
    """Muestra las opciones dentro de la pregunta, en el mismo formulario."""

    model = Choice
    extra = 3


class QuestionInline(admin.TabularInline):
    """Muestra las preguntas dentro del examen, en el mismo formulario."""

    model = Question
    extra = 1


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("title", "description")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "exam")
    list_filter = ("exam",)
    search_fields = ("text",)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "question", "is_correct")
    list_filter = ("is_correct", "question__exam")
    search_fields = ("text",)
