from django.contrib import admin
from .models import (
    Classroom,
    Subject,
    SubjectTeacherAssignment,
    AcademicTerm,
    Mark,
    BehaviorAssessment,
    TimetableSlot,
)


@admin.register(AcademicTerm)
class AcademicTermAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'class_teacher')
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    filter_horizontal = ('classrooms',)


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'academic_term', 'test1', 'test2', 'test3', 'average')
    list_filter = ('academic_term', 'classroom', 'subject')
    search_fields = ('student__first_name', 'student__last_name', 'student__admission_number')


@admin.register(BehaviorAssessment)
class BehaviorAssessmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'classroom', 'academic_term', 'evaluated_by', 'updated_at')
    list_filter = ('academic_term', 'classroom')


@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'day_of_week', 'subject', 'teacher', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'classroom', 'teacher')
    search_fields = ('classroom__name', 'subject__name', 'teacher__username', 'teacher__first_name')