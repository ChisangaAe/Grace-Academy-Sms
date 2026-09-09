from django.db import models
from django.conf import settings
from students.models import Student

DAY_CHOICES = [
    ('MONDAY', 'Monday'),
    ('TUESDAY', 'Tuesday'),
    ('WEDNESDAY', 'Wednesday'),
    ('THURSDAY', 'Thursday'),
    ('FRIDAY', 'Friday'),
]


class Classroom(models.Model):
    LEVEL_CHOICES = [
        ('PRIMARY', 'Primary'),
        ('SECONDARY', 'Secondary'),
    ]
    SECTION_CHOICES = [
        ('GRADE_5', 'Grade 5'),
        ('GRADE_6', 'Grade 6'),
        ('PRIMARY', 'Primary Section'),
        ('SECONDARY', 'Secondary Section'),
    ]

    name = models.CharField(max_length=50)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='SECONDARY')
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='PRIMARY')
    capacity = models.PositiveIntegerField(default=40)
    class_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='managed_classrooms',
        help_text="Assigned class teacher"
    )

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    classrooms = models.ManyToManyField(Classroom, related_name='subjects', blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class SubjectTeacherAssignment(models.Model):
    """Assigns specific subject teachers to a subject in a specific classroom."""
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subject_assignments')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='subject_assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_assignments')

    class Meta:
        unique_together = ('teacher', 'classroom', 'subject')

    def __str__(self):
        teacher_name = self.teacher.get_full_name() or self.teacher.username
        return f"{teacher_name} -> {self.subject.name} ({self.classroom.name})"


class AcademicTerm(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    end_date = models.DateField(null=True, blank=True)
    next_term_start = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    academic_term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)

    test1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    test2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    test3 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    average = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'subject', 'academic_term')

    def save(self, *args, **kwargs):
        scores = [score for score in [self.test1, self.test2, self.test3] if score is not None]
        if scores:
            self.average = round(sum(scores) / len(scores), 2)
        else:
            self.average = None
        super().save(*args, **kwargs)


class BehaviorAssessment(models.Model):
    RATING_CHOICES = [
        ('EXCELLENT', 'A - Excellent'),
        ('VERY_GOOD', 'B - Very Good'),
        ('GOOD', 'C - Good'),
        ('SATISFACTORY', 'D - Satisfactory'),
        ('NEEDS_IMPROVEMENT', 'E - Needs Improvement'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='behavior_assessments')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    academic_term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)

    # Personal Behaviour & Character Items
    obedience = models.CharField(max_length=25, choices=RATING_CHOICES, default='GOOD')
    self_control = models.CharField(max_length=25, choices=RATING_CHOICES, default='GOOD')
    sports = models.CharField(max_length=25, choices=RATING_CHOICES, default='GOOD')
    honesty = models.CharField(max_length=25, choices=RATING_CHOICES, default='GOOD')
    homework = models.CharField(max_length=25, choices=RATING_CHOICES, default='GOOD')
    cheerfulness = models.CharField(max_length=25, choices=RATING_CHOICES, default='GOOD')
    leadership = models.CharField(max_length=25, choices=RATING_CHOICES, default='GOOD')
    helpfulness = models.CharField(max_length=25, choices=RATING_CHOICES, default='GOOD')
    neatness = models.CharField(max_length=25, choices=RATING_CHOICES, default='GOOD')
    responsibility = models.CharField(max_length=25, choices=RATING_CHOICES, default='GOOD')
    stewardship = models.CharField(max_length=25, choices=RATING_CHOICES, default='GOOD')

    # Remarks
    class_teacher_remark = models.TextField(blank=True, null=True, help_text="Class Teacher Remarks")
    head_teacher_remark = models.TextField(blank=True, null=True, help_text="Principal / Head Teacher Remarks")
    
    evaluated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'academic_term')

    def __str__(self):
        return f"Behavior: {self.student.get_full_name()} ({self.academic_term})"


class TimetableSlot(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='timetable_slots')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='timetable_slots'
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES, default='MONDAY')
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.classroom.name} | {self.get_day_of_week_display()} ({self.start_time} - {self.end_time})"