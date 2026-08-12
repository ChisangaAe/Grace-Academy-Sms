from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Grade
from .forms import GradeForm
from academics.models import Subject

def grade_list(request):
    query = request.GET.get('q', '')
    subject_filter = request.GET.get('subject', '')
    type_filter = request.GET.get('assessment_type', '')

    grades = Grade.objects.select_related('student', 'subject').all()

    # Filter by student name or admission number
    if query:
        grades = grades.filter(
            Q(student__first_name__icontains=query) |
            Q(student__last_name__icontains=query) |
            Q(student__admission_number__icontains=query)
        )

    # Filter by subject
    if subject_filter:
        grades = grades.filter(subject_id=subject_filter)

    # Filter by assessment type
    if type_filter:
        grades = grades.filter(assessment_type=type_filter)

    subjects = Subject.objects.all()

    context = {
        'grades': grades,
        'subjects': subjects,
        'query': query,
        'selected_subject': subject_filter,
        'selected_type': type_filter,
        'assessment_types': Grade.ASSESSMENT_TYPES,
    }
    return render(request, 'grades/grade_list.html', context)

def add_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'grades/grade_form.html', {'form': form})