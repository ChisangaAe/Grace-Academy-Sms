from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Attendance
from .forms import AttendanceForm

def attendance_list(request):
    query = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    status_filter = request.GET.get('status', '')

    attendances = Attendance.objects.select_related('student', 'student__classroom').all()

    # Filter by student name or admission number
    if query:
        attendances = attendances.filter(
            Q(student__first_name__icontains=query) |
            Q(student__last_name__icontains=query) |
            Q(student__admission_number__icontains=query)
        )

    # Filter by date
    if date_filter:
        attendances = attendances.filter(date=date_filter)

    # Filter by status
    if status_filter:
        attendances = attendances.filter(status=status_filter)

    context = {
        'attendances': attendances,
        'query': query,
        'selected_date': date_filter,
        'selected_status': status_filter,
        'status_choices': Attendance.STATUS_CHOICES,
    }
    return render(request, 'attendance/attendance_list.html', context)

def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/attendance_form.html', {'form': form})