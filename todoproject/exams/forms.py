from django import forms
from django.forms import inlineformset_factory

from .models import Choice, Exam, Question


class ExamForm(forms.ModelForm):
    """Formulario para crear un examen (solo el encabezado)."""

    class Meta:
        model = Exam
        fields = ["title", "description", "active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class QuestionForm(forms.ModelForm):
    """Formulario de UNA pregunta. No guarda la pregunta todavia: la vista
    guarda primero la pregunta y despues las opciones con el formset."""

    class Meta:
        model = Question
        fields = ["text"]
        labels = {"text": "Texto de la pregunta"}
        widgets = {
            "text": forms.TextInput(
                attrs={"class": "w-full border rounded px-3 py-2"}
            ),
        }


class ChoiceForm(forms.ModelForm):
    """Formulario de UNA opcion de respuesta."""

    class Meta:
        model = Choice
        fields = ["text", "is_correct"]
        labels = {"text": "Opcion", "is_correct": "Es la correcta"}


# Formset de opciones: permite agregar varias opciones de una sola vez.
ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    form=ChoiceForm,
    extra=3,          # 3 filas vacias
    min_num=2,        # minimo 2 opciones por pregunta
    validate_min=True,
    can_delete=True,
)


def clean_choices(formset):
    """Valida que exista EXACTAMENTE UNA opcion marcada como correcta.

    Devuelve (formset, error). Si todo esta bien, error es None.
    """
    if not formset.is_valid():
        return formset, "Revisa los datos de las opciones."

    correctas = 0
    for form in formset.forms:
        if not form.cleaned_data or form.cleaned_data.get("DELETE"):
            continue
        if form.cleaned_data.get("is_correct"):
            correctas += 1

    if correctas == 0:
        return formset, "Debe existir al menos una opcion correcta."
    if correctas > 1:
        return formset, "Solo puede existir UNA opcion correcta por pregunta."

    return formset, None
