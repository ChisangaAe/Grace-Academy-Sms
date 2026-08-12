from django.db import models
from students.models import Student

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    remarks = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.date} ({self.get_status_display()})"