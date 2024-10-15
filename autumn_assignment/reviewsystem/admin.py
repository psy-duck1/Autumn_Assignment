from django.contrib import admin
from .models import Team, SubTask, TeamAssignment, Assignment

admin.site.register(Team)
admin.site.register(SubTask)
admin.site.register(Assignment)
