from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Custom fields
    username = models.CharField(max_length=50)
    enrollment_no = models.CharField(max_length=8, unique=True)  # Initially allow null
    email = models.EmailField(('email address'), unique=True)
    date_of_joining = models.DateField(null=True)
    phone_no = models.CharField(max_length=10, null=True, blank=True, default='00')
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional profile picture field (uncomment if needed)
    # profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    # Custom groups and permissions (if using Django's auth system)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
    )
    # Custom authentication fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Remove 'enrollment_no' from REQUIRED_FIELDS for now

    def __str__(self):
        return self.username
class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name='roles',
        null=True,  # Allow null values temporarily
        default=None  # Set a default value
    )

    class Meta:
        unique_together = ('name', 'organization')

    def __str__(self):
        return f"{self.name} at {self.organization.name if self.organization else 'No Organization'}"
class UserOrganizationRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'organization', 'role')

    def __str__(self):
        return f"{self.user.username} - {self.role.name} at {self.organization.name}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.team.name} - {self.user.username}"

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title

class AssignmentRole(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user_organization_role = models.ForeignKey(
        UserOrganizationRole, 
        on_delete=models.CASCADE, 
        null=True,  # Allow null values temporarily
        default=None  # Set a default value
    )

    class Meta:
        unique_together = ('assignment', 'user_organization_role')

    def __str__(self):
        return f"{self.assignment.title} - {self.user_organization_role}"

class TeamAssignment(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('team', 'assignment')

    def __str__(self):
        return f"{self.team.name} - {self.assignment.title}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    iteration_no = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.assignment.title} - Submission {self.iteration_no}"

class SubmissionAttachment(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.submission} - {self.file_name}"

class SubmissionScore(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    total_score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.submission} - Score: {self.total_score}"

class SubTask(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    description = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.assignment.title} - Subtask"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment.title} - Comment by {self.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

class NotificationSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    realtime_updates = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification Settings for {self.user.username}"