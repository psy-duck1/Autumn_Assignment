from django.contrib import admin
from .models import (
    User,
    Organization,
    Role,
    UserOrganizationRole,
    Team,
    TeamMember,
    Assignment,
    AssignmentRole,
    TeamAssignment,
    Submission,
    SubmissionAttachment,
    SubmissionScore,
    SubTask,
    Comment,
    Notification,
    NotificationSetting
)

# Register all models
admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Role)
admin.site.register(UserOrganizationRole)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Assignment)
admin.site.register(AssignmentRole)
admin.site.register(TeamAssignment)
admin.site.register(Submission)
admin.site.register(SubmissionAttachment)
admin.site.register(SubmissionScore)
admin.site.register(SubTask)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(NotificationSetting)

