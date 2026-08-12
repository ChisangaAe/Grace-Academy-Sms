from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Classroom, Subject, AcademicTerm, Mark, BehaviorAssessment, SubjectTeacherAssignment
from .forms import ClassroomForm, SubjectForm, BehaviorAssessmentForm
from students.models import Student

User = get_user_model()


def is_deputy_or_admin(user):
    """Helper to check if a user is a Deputy Head or Superuser."""
    return user.is_superuser or user.groups.filter(name='Deputy Head').exists()


# --- CLASSROOM VIEWS ---

@login_required
def classroom_list(request):
    classrooms = Classroom.objects.all()
    return render(request, 'academics/classroom_list.html', {'classrooms': classrooms})

@login_required
def classroom_create(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Classroom created successfully.")
            return redirect('classroom_list')
    else:
        form = ClassroomForm()
    return render(request, 'academics/classroom_form.html', {'form': form, 'title': 'Create Classroom'})


# --- SUBJECT VIEWS ---

@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'academics/subject_list.html', {'subjects': subjects})

@login_required
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject created successfully.")
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'academics/subject_form.html', {'form': form, 'title': 'Create Subject'})


# --- DEPUTY HEAD ASSIGNMENT VIEWS ---

@login_required
def assign_class_teacher(request):
    """Deputy Head / Admin view to assign Class Teachers across Grade 5, 6, and Secondary."""
    if not is_deputy_or_admin(request.user):
        messages.error(request, "Access Denied: Only the Deputy Head or Admin can assign Class Teachers.")
        return redirect('dashboard')

    classrooms = Classroom.objects.all().order_by('section', 'name')
    teachers = User.objects.filter(is_active=True)

    if request.method == 'POST':
        classroom_id = request.POST.get('classroom_id')
        teacher_id = request.POST.get('teacher_id')

        classroom = get_object_or_404(Classroom, pk=classroom_id)
        teacher = User.objects.filter(pk=teacher_id).first() if teacher_id else None

        classroom.class_teacher = teacher
        classroom.save()

        teacher_name = teacher.get_full_name() or teacher.username if teacher else "None"
        messages.success(request, f"Assigned {teacher_name} as Class Teacher for {classroom.name}.")
        return redirect('assign_class_teacher')

    context = {
        'classrooms': classrooms,
        'teachers': teachers,
    }
    return render(request, 'academics/assign_class_teacher.html', context)


@login_required
def assign_subject_teacher(request):
    """Deputy Head / Admin view to assign Subject Teachers to specific subjects and classrooms."""
    if not is_deputy_or_admin(request.user):
        messages.error(request, "Access Denied: Only the Deputy Head or Admin can assign Subject Teachers.")
        return redirect('dashboard')

    assignments = SubjectTeacherAssignment.objects.select_related('teacher', 'classroom', 'subject').all()
    classrooms = Classroom.objects.all()
    subjects = Subject.objects.all()
    teachers = User.objects.filter(is_active=True)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'assign':
            teacher_id = request.POST.get('teacher_id')
            classroom_id = request.POST.get('classroom_id')
            subject_id = request.POST.get('subject_id')

            teacher = get_object_or_404(User, pk=teacher_id)
            classroom = get_object_or_404(Classroom, pk=classroom_id)
            subject = get_object_or_404(Subject, pk=subject_id)

            SubjectTeacherAssignment.objects.get_or_create(
                teacher=teacher,
                classroom=classroom,
                subject=subject
            )
            messages.success(request, f"Assigned {teacher.get_full_name() or teacher.username} to teach {subject.name} in {classroom.name}.")

        elif action == 'remove':
            assignment_id = request.POST.get('assignment_id')
            SubjectTeacherAssignment.objects.filter(pk=assignment_id).delete()
            messages.success(request, "Subject teacher assignment removed.")

        return redirect('assign_subject_teacher')

    context = {
        'assignments': assignments,
        'classrooms': classrooms,
        'subjects': subjects,
        'teachers': teachers,
    }
    return render(request, 'academics/assign_subject_teacher.html', context)


# --- MARKS & BEHAVIOR VIEWS ---

@login_required
def enter_marks(request):
    """Subject teachers enter Test 1, Test 2, and Test 3 scores only for their assigned subjects/classes."""
    user = request.user
    terms = AcademicTerm.objects.all()

    # Filter available classrooms & subjects based on teacher assignments
    if is_deputy_or_admin(user):
        classrooms = Classroom.objects.all()
        subjects = Subject.objects.all()
    else:
        assigned_pairs = SubjectTeacherAssignment.objects.filter(teacher=user)
        classrooms = Classroom.objects.filter(id__in=assigned_pairs.values_list('classroom_id', flat=True)).distinct()
        subjects = Subject.objects.filter(id__in=assigned_pairs.values_list('subject_id', flat=True)).distinct()

    selected_classroom_id = request.GET.get('classroom') or request.POST.get('classroom')
    selected_subject_id = request.GET.get('subject') or request.POST.get('subject')
    selected_term_id = request.GET.get('term') or request.POST.get('term')

    mark_data = []

    if selected_classroom_id and selected_subject_id and selected_term_id:
        classroom = get_object_or_404(Classroom, pk=selected_classroom_id)
        subject = get_object_or_404(Subject, pk=selected_subject_id)
        term = get_object_or_404(AcademicTerm, pk=selected_term_id)

        # Enforce subject teacher permission check
        if not is_deputy_or_admin(user):
            is_assigned = SubjectTeacherAssignment.objects.filter(
                teacher=user,
                classroom=classroom,
                subject=subject
            ).exists()
            if not is_assigned:
                messages.error(request, f"Access Restricted: You are not assigned to teach {subject.name} in {classroom.name}.")
                return redirect('enter_marks')

        students = Student.objects.filter(classroom=classroom, is_active=True)

        if request.method == 'POST':
            def parse_score(val):
                if val is not None and str(val).strip() != '':
                    try:
                        return Decimal(str(val).strip())
                    except (InvalidOperation, ValueError):
                        return None
                return None

            for student in students:
                t1 = parse_score(request.POST.get(f"test1_{student.id}"))
                t2 = parse_score(request.POST.get(f"test2_{student.id}"))
                t3 = parse_score(request.POST.get(f"test3_{student.id}"))

                mark_obj, _ = Mark.objects.get_or_create(
                    student=student,
                    subject=subject,
                    academic_term=term,
                    defaults={'classroom': classroom}
                )

                mark_obj.classroom = classroom
                mark_obj.test1 = t1
                mark_obj.test2 = t2
                mark_obj.test3 = t3
                mark_obj.save()  # Triggers average calculation in Mark.save()

            messages.success(request, f"Marks updated successfully for {subject.name} - {classroom.name}.")
            return redirect(f"{request.path}?classroom={selected_classroom_id}&subject={selected_subject_id}&term={selected_term_id}")

        for student in students:
            mark = Mark.objects.filter(student=student, subject=subject, academic_term=term).first()
            mark_data.append({
                'student': student,
                'mark': mark
            })

    context = {
        'classrooms': classrooms,
        'subjects': subjects,
        'terms': terms,
        'selected_classroom_id': int(selected_classroom_id) if selected_classroom_id and str(selected_classroom_id).isdigit() else None,
        'selected_subject_id': int(selected_subject_id) if selected_subject_id and str(selected_subject_id).isdigit() else None,
        'selected_term_id': int(selected_term_id) if selected_term_id and str(selected_term_id).isdigit() else None,
        'mark_data': mark_data,
    }
    return render(request, 'academics/enter_marks.html', context)


@login_required
def enter_behavior(request):
    """Personal Behaviour & Character assessment, ONLY accessible by assigned Class Teacher or Deputy/Admin."""
    classrooms = Classroom.objects.all()
    terms = AcademicTerm.objects.all()

    selected_classroom_id = request.GET.get('classroom') or request.POST.get('classroom')
    selected_term_id = request.GET.get('term') or request.POST.get('term')

    is_class_teacher = False
    student_evaluations = []

    if selected_classroom_id and selected_term_id:
        classroom = get_object_or_404(Classroom, pk=selected_classroom_id)
        term = get_object_or_404(AcademicTerm, pk=selected_term_id)

        # Permission check: Class Teacher, Deputy Head, or Admin
        if request.user == classroom.class_teacher or is_deputy_or_admin(request.user):
            is_class_teacher = True
        else:
            messages.error(request, f"Access Restricted: Only {classroom.class_teacher or 'the assigned Class Teacher'} can enter character assessments for {classroom.name}.")
            return redirect('dashboard')

        students = Student.objects.filter(classroom=classroom, is_active=True)

        if request.method == 'POST' and is_class_teacher:
            for student in students:
                assessment, _ = BehaviorAssessment.objects.get_or_create(
                    student=student,
                    academic_term=term,
                    defaults={'classroom': classroom}
                )

                # Save all 11 character items matching the report card layout
                assessment.obedience = request.POST.get(f"obedience_{student.id}", 'GOOD')
                assessment.self_control = request.POST.get(f"self_control_{student.id}", 'GOOD')
                assessment.sports = request.POST.get(f"sports_{student.id}", 'GOOD')
                assessment.honesty = request.POST.get(f"honesty_{student.id}", 'GOOD')
                assessment.homework = request.POST.get(f"homework_{student.id}", 'GOOD')
                assessment.cheerfulness = request.POST.get(f"cheerfulness_{student.id}", 'GOOD')
                assessment.leadership = request.POST.get(f"leadership_{student.id}", 'GOOD')
                assessment.helpfulness = request.POST.get(f"helpfulness_{student.id}", 'GOOD')
                assessment.neatness = request.POST.get(f"neatness_{student.id}", 'GOOD')
                assessment.responsibility = request.POST.get(f"responsibility_{student.id}", 'GOOD')
                assessment.stewardship = request.POST.get(f"stewardship_{student.id}", 'GOOD')

                assessment.class_teacher_remark = request.POST.get(f"teacher_remark_{student.id}")
                if is_deputy_or_admin(request.user):
                    assessment.head_teacher_remark = request.POST.get(f"head_remark_{student.id}")

                assessment.evaluated_by = request.user
                assessment.save()

            messages.success(request, f"Personal Behaviour & Character evaluations saved for {classroom.name}.")
            return redirect(f"{request.path}?classroom={selected_classroom_id}&term={selected_term_id}")

        for student in students:
            eval_obj = BehaviorAssessment.objects.filter(student=student, academic_term=term).first()
            form = BehaviorAssessmentForm(instance=eval_obj) if eval_obj else BehaviorAssessmentForm()
            student_evaluations.append({
                'student': student,
                'form': form,
                'eval': eval_obj
            })

    context = {
        'classrooms': classrooms,
        'terms': terms,
        'selected_classroom_id': int(selected_classroom_id) if selected_classroom_id and str(selected_classroom_id).isdigit() else None,
        'selected_term_id': int(selected_term_id) if selected_term_id and str(selected_term_id).isdigit() else None,
        'student_evaluations': student_evaluations,
        'is_class_teacher': is_class_teacher,
    }
    return render(request, 'academics/enter_behavior.html', context)