from django.db import models


class GradeScale(models.Model):
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, null=True, blank=True)
    min_score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    grade_letter = models.CharField(max_length=5)
    remarks = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.grade_letter} ({self.min_score} - {self.max_score})"


class Grade(models.Model):
    ASSESSMENT_TYPES = [
        ('Assignment', 'Assignment'),
        ('Quiz', 'Quiz'),
        ('Midterm', 'Midterm Exam'),
        ('Final', 'Final Exam'),
    ]

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='grades')
    assessment_type = models.CharField(max_length=50, choices=ASSESSMENT_TYPES, default='Final')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    date_added = models.DateField(auto_now_add=True)

    def percentage(self):
        if self.max_score > 0:
            return round((self.score / self.max_score) * 100, 1)
        return 0

    def letter_grade(self):
        pct = self.percentage()
        if pct >= 80:
            return 'A'
        elif pct >= 70:
            return 'B'
        elif pct >= 60:
            return 'C'
        elif pct >= 50:
            return 'D'
        else:
            return 'F'

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}/{self.max_score}"