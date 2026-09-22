import csv
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Student
from academics.models import Mark, BehaviorAssessment, AcademicTerm, Classroom, Subject
from django.shortcuts import render

def calculate_grade_and_remark(score):
    """Calculates grade number and remark based on performance score."""
    if score is None:
        return "-", "-"
    try:
        val = float(score)
    except (ValueError, TypeError):
        return "-", "-"

    if val >= 95:
        return "1", "Excellent"
    elif val >= 90:
        return "2", "Very Good"
    elif val >= 80:
        return "3", "Good"
    elif val >= 70:
        return "4", "Pass"
    elif val >= 60:
        return "5", "Fair"
    elif val >= 50:
        return "6", "Below Avg."
    elif val >= 40:
        return "7", "Satisfactory"
    else:
        return "8", "Unsatisfactory"


@login_required
def dashboard(request):
    """Main system dashboard view."""
    total_students = Student.objects.filter(is_active=True).count()
    total_classrooms = Classroom.objects.count()
    total_subjects = Subject.objects.count()

    context = {
        'total_students': total_students,
        'total_classrooms': total_classrooms,
        'total_subjects': total_subjects,
    }
    return render(request, 'dashboard.html', context)


@login_required
def student_list(request):
    """List all active students."""
    students = Student.objects.filter(is_active=True)
    return render(request, 'students/student_list.html', {'students': students})


@login_required
def student_detail(request, pk):
    """Student profile view."""
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


@login_required
def student_create(request):
    """Create new student record."""
    return render(request, 'students/student_form.html')


@login_required
def student_update(request, pk):
    """Update student record."""
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_form.html', {'student': student})


@login_required
def delete_student(request, pk):
    """Deactivate or delete student."""
    student = get_object_or_404(Student, pk=pk)
    student.is_active = False
    student.save()
    messages.success(request, f"Student {student} deactivated successfully.")
    return redirect('student_list')


@login_required
def export_students_csv(request):
    """Export student roster to CSV."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_roster.csv"'
    writer = csv.writer(response)
    writer.writerow(['Admission Number', 'First Name', 'Last Name', 'Classroom'])
    for student in Student.objects.filter(is_active=True):
        writer.writerow([student.admission_number, student.first_name, student.last_name, student.classroom])
    return response


@login_required
def generate_id_card(request, pk):
    """Generate printable student ID card."""
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/id_card.html', {'student': student})


@login_required
def student_report_card(request, student_id):
    """Display student academic & behavior report card."""
    student = get_object_or_404(Student, pk=student_id)
    terms = AcademicTerm.objects.all()
    
    selected_term_id = request.GET.get('term')
    if selected_term_id and selected_term_id.isdigit():
        term = AcademicTerm.objects.filter(pk=int(selected_term_id)).first()
    else:
        term = terms.last()
        
    marks = []
    behavior = None
    overall_average = Decimal('0.00')

    if term:
        marks = Mark.objects.filter(student=student, academic_term=term).select_related('subject')
        behavior = BehaviorAssessment.objects.filter(student=student, academic_term=term).first()
        
        # Calculate dynamic grade and remark based on average score for each subject
        for mark in marks:
            grade, remark = calculate_grade_and_remark(mark.average)
            mark.calculated_grade = grade
            mark.calculated_remark = remark

        valid_averages = [m.average for m in marks if m.average is not None]
        if valid_averages:
            overall_average = round(sum(valid_averages) / len(valid_averages), 2)

    context = {
        'student': student,
        'terms': terms,
        'selected_term': term,
        'marks': marks,
        'behavior': behavior,
        'overall_average': overall_average,
    }
    return render(request, 'students/report_card.html', context)


@login_required
def bulk_assign_classroom(request):
    """Bulk assign classroom to students."""
    return render(request, 'students/bulk_assign.html')


@login_required
def bulk_promote(request):
    """Bulk promote students to next grade."""
    return render(request, 'students/bulk_promote.html')
def teacher_list(request):
    return render(request, 'placeholder.html', {'module_name': 'Teachers & Staff'})

def classroom_list(request):
    return render(request, 'placeholder.html', {'module_name': 'Classrooms'})

def attendance_list(request):
    return render(request, 'placeholder.html', {'module_name': 'Attendance'})

def examination_list(request):
    return render(request, 'placeholder.html', {'module_name': 'Examination & Marks'})

def finance_dashboard(request):
    return render(request, 'placeholder.html', {'module_name': 'Finance & Fees'})

def system_settings(request):
    return render(request, 'placeholder.html', {'module_name': 'System Settings'})

def promote_class(request):
    return render(request, 'placeholder.html', {'module_name': 'Promote Class'})