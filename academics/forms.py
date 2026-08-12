from django import forms
from .models import Classroom, Subject, BehaviorAssessment


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'section', 'capacity', 'class_teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-select'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'class_teacher': forms.Select(attrs={'class': 'form-select'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'classrooms']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'classrooms': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }


class BehaviorAssessmentForm(forms.ModelForm):
    class Meta:
        model = BehaviorAssessment
        fields = [
            'obedience',
            'self_control',
            'sports',
            'honesty',
            'homework',
            'cheerfulness',
            'leadership',
            'helpfulness',
            'neatness',
            'responsibility',
            'stewardship',
            'class_teacher_remark',
            'head_teacher_remark',
        ]
        widgets = {
            'obedience': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'self_control': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'sports': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'honesty': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'homework': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'cheerfulness': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'leadership': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'helpfulness': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'neatness': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'responsibility': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'stewardship': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'class_teacher_remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'head_teacher_remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }