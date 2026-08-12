from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'username', 'first_name', 'last_name', 'role', 
        'section', 'is_approved', 'primary_class', 'get_subjects'
    )
    list_filter = ('role', 'section', 'is_approved', 'is_staff')
    
    # Fields displayed in editing view
    fieldsets = UserAdmin.fieldsets + (
        ('School Role & Approval', {
            'fields': ('role', 'section', 'is_approved')
        }),
        ('Teacher Assignments', {
            'fields': ('primary_class', 'secondary_subjects'),
            'description': 'Map Primary/ECE teachers to a class, or Secondary teachers to 1-2 subjects.'
        }),
    )

    # Admin actions for batch approval by the Principal
    actions = ['approve_accounts', 'revoke_approval']

    @admin.action(description="Approve selected teacher accounts")
    def approve_accounts(self, request, queryset):
        queryset.update(is_approved=True, is_active=True)
        self.message_user(request, "Selected accounts have been approved successfully.")

    @admin.action(description="Revoke approval for selected accounts")
    def revoke_approval(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected account approvals have been revoked.")

    def get_subjects(self, obj):
        return ", ".join([s.name for s in obj.secondary_subjects.all()])
    get_subjects.short_description = 'Secondary Subjects'