# apps/training/admin/instructor.py
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

@admin.register(TrainingSession)
class InstructorTrainingAdmin(admin.ModelAdmin):
    list_display = ('student', 'schedule', 'status', 'vehicle')
    list_filter = ('status', 'schedule')
    search_fields = ('student__username',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'instructor':
            return qs.filter(instructor__user=request.user)
        return qs

    @method_decorator(staff_member_required)
    def has_module_permission(self, request):
        return request.user.role in ['admin', 'instructor']

# Template khusus di templates/admin/instructor/index.html