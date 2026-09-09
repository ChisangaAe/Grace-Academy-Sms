from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Role Levels
    ROLE_CHOICES = (
        ('IT_TECH', 'IT Technician (Super Admin)'),
        ('PRINCIPAL', 'Principal (Super Admin)'),
        ('DEPUTY_PRIMARY', 'Deputy Head - Primary & ECE (Admin)'),
        ('DEPUTY_SECONDARY', 'Deputy Head - Secondary (Admin)'),
        ('TEACHER', 'Teacher (Regular User)'),
    )

    # School Sections
    SECTION_CHOICES = (
        ('ECE', 'ECE (Early Childhood)'),
        ('PRIMARY', 'Primary Section'),
        ('SECONDARY', 'Secondary Section'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TEACHER')
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, blank=True, null=True)
    
    # Approval status
    is_approved = models.BooleanField(
        default=False, 
        help_text="Requires approval before user can log in."
    )

    # Avoid reverse accessor conflicts with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="account_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="account_user_permissions",
        related_query_name="user",
    )

    # Primary & ECE Teacher Mapping: Mapped to a single classroom
    primary_class = models.ForeignKey(
        'academics.Classroom',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_class_users',
        help_text="Assigned Class (For ECE & Primary Teachers)"
    )

    # Secondary Teacher Mapping: Mapped to subjects
    secondary_subjects = models.ManyToManyField(
        'academics.Subject',
        blank=True,
        related_name='subject_teachers',
        help_text="Assigned Subjects (For Secondary Teachers)"
    )

    @property
    def is_super_admin(self):
        """Returns True if IT Technician, Principal, or Django Superuser."""
        return self.role in ['IT_TECH', 'PRINCIPAL'] or self.is_superuser

    @property
    def is_admin_user(self):
        """Returns True if IT Tech, Principal, or Deputy Head."""
        return self.role in ['IT_TECH', 'PRINCIPAL', 'DEPUTY_PRIMARY', 'DEPUTY_SECONDARY'] or self.is_staff

    @property
    def is_allocated(self):
        """Dynamic check if teacher has section and class/subjects assigned."""
        if self.is_admin_user:
            return True

        if not self.is_approved or not self.section:
            return False

        if self.section in ['ECE', 'PRIMARY']:
            return self.primary_class is not None

        if self.section == 'SECONDARY':
            return self.secondary_subjects.exists()

        return False

    def save(self, *args, **kwargs):
        """Automatically assign staff/superuser rights based on role."""
        if self.role in ['IT_TECH', 'PRINCIPAL']:
            self.is_staff = True
            self.is_superuser = True
            self.is_approved = True
        elif self.role in ['DEPUTY_PRIMARY', 'DEPUTY_SECONDARY']:
            self.is_staff = True
            self.is_approved = True
            
        super().save(*args, **kwargs)

    def __str__(self):
        full_name = self.get_full_name()
        return f"{full_name if full_name else self.username} - {self.get_role_display()}"