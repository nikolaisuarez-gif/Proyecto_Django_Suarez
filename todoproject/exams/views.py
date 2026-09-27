from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChoiceFormSet, ExamForm, QuestionForm, clean_choices
from .models import Exam, Question


def exam_list(request):
    """Lista todos los examenes con su numero de preguntas."""
    exams = Exam.objects.all()
    return render(request, "exams/exam_list.html", {"exams": exams})


def exam_detail(request, pk):
    """Muestra un examen con todas sus preguntas y opciones."""
    exam = get_object_or_404(Exam, pk=pk)
    return render(
        request, "exams/exam_detail.html", {"exam": exam, "questions": exam.questions.all()}
    )


def exam_create(request):
    """Crea un examen con UNA pregunta y sus opciones usando el formset."""
    if request.method == "POST":
        form = ExamForm(request.POST)
        question_form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        if form.is_valid() and question_form.is_valid() and formset.is_valid():
            _, error = clean_choices(formset)
            if error:
                formset = ChoiceFormSet(request.POST)
                formset.is_valid()
                formset.non_form_errors = error
            else:
                exam = form.save()
                question = question_form.save(commit=False)
                question.exam = exam
                question.save()
                formset.instance = question
                formset.save()
                return redirect("exams:exam_detail", pk=exam.pk)
    else:
        form = ExamForm()
        question_form = QuestionForm()
        formset = ChoiceFormSet()

    return render(
        request,
        "exams/exam_form.html",
        {"form": form, "question_form": question_form, "formset": formset},
    )


def question_add(request, pk):
    """Agrega una pregunta (con sus opciones) a un examen existente."""
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        if question_form.is_valid() and formset.is_valid():
            _, error = clean_choices(formset)
            if error:
                formset = ChoiceFormSet(request.POST)
                formset.is_valid()
                formset.non_form_errors = error
            else:
                question = question_form.save(commit=False)
                question.exam = exam
                question.save()
                formset.instance = question
                formset.save()
                return redirect("exams:exam_detail", pk=exam.pk)
    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet()

    return render(
        request,
        "exams/question_form.html",
        {"exam": exam, "question_form": question_form, "formset": formset},
    )


def question_detail(request, pk):
    """Muestra una pregunta con sus opciones."""
    question = get_object_or_404(Question, pk=pk)
    return render(
        request,
        "exams/question_detail.html",
        {"question": question, "choices": question.choices.all()},
    )
