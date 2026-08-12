from django import forms
from .models import Student
from academics.models import Classroom

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'admission_number', 'gender', 'section', 'classroom', 'guardian_name', 'guardian_phone', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'admission_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'section': forms.Select(attrs={'class': 'form-select'}),
            'classroom': forms.Select(attrs={'class': 'form-select'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class BulkAssignForm(forms.Form):
    target_classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.all(),
        required=False,
        empty_label="-- Select Target Classroom --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    target_section = forms.ChoiceField(
        choices=[('', '-- Select Target Section --')] + list(Student.SECTION_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class BulkPromoteForm(forms.Form):
    from_classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.all(),
        required=True,
        empty_label="-- Current Classroom (From) --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    to_classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.all(),
        required=False,
        empty_label="-- Next Classroom (To) / Leave blank to unassign --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )