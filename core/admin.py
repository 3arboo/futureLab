from django.contrib import admin
from .models import CustomUser, Project, Evaluation, StudentAssignment

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id_student', 'full_name', 'role', 'project', 'phone']
    list_filter = ['role', 'project']
    search_fields = ['id_student', 'full_name', 'phone']
    ordering = ['full_name']
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('id_student', 'full_name', 'role')
        }),
        ('معلومات إضافية', {
            'fields': ('phone', 'project')
        }),
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'presentation_time', 'location', 'get_students_count']
    list_filter = ['presentation_time', 'location']
    search_fields = ['title', 'description', 'location']
    ordering = ['-presentation_time']

    def get_students_count(self, obj):
        return obj.students.count()
    get_students_count.short_description = 'عدد الطلاب'

class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['project', 'evaluator_name', 'rating', 'created_at']
    list_filter = ['project', 'rating', 'created_at']
    search_fields = ['project__title', 'evaluator_name', 'comments']
    readonly_fields = ['created_at']

admin.site.register(Evaluation, EvaluationAdmin)

@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'project', 'submitted_at']
    list_filter = ['project', 'submitted_at']
    search_fields = ['student__username', 'project__title']
