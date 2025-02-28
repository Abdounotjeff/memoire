from django.contrib import admin
from .models import ProjectSubmissionTask

class ProjectSubmissionTaskAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "groups":
            if request.user.is_authenticated and hasattr(request.user, 'professor'):
                kwargs["queryset"] = request.user.professor.groups.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(ProjectSubmissionTask, ProjectSubmissionTaskAdmin)
