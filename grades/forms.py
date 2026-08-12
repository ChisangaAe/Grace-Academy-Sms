from django import forms
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'assessment_type', 'score', 'max_score']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'assessment_type': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'e.g. 85.5'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'value': '100'}),
        }