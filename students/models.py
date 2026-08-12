import datetime
from django.db import models


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    SECTION_CHOICES = (
        ('ECE', 'ECE'),
        ('PRIMARY', 'Primary Section'),
        ('SECONDARY', 'Secondary Section'),
    )

    admission_number = models.CharField(
        max_length=30, 
        unique=True, 
        blank=True, 
        help_text="Auto-generated e.g. GA-2026-001"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField(blank=True, null=True)
    
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='PRIMARY')
    
    # Passed 'academics.Classroom' as a string reference to fix circular import
    classroom = models.ForeignKey(
        'academics.Classroom', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='students'
    )

    # Parent / Guardian Details
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Passport Photo
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.admission_number:
            current_year = datetime.datetime.now().year
            prefix = f"GA-{current_year}-"
            
            # Find the last student with an admission number starting with this prefix
            last_student = Student.objects.filter(
                admission_number__startswith=prefix
            ).order_by('id').last()
            
            if last_student and last_student.admission_number:
                try:
                    # Extract numeric part from the end (e.g. GA-2026-005 -> 5)
                    last_num = int(last_student.admission_number.split('-')[-1])
                    next_number = last_num + 1
                except ValueError:
                    next_number = 1
            else:
                next_number = 1
            
            self.admission_number = f"{prefix}{next_number:03d}"
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.admission_number} - {self.first_name} {self.last_name}"  