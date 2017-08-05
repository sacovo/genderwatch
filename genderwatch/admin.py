from django.contrib import admin
from genderwatch.models import Assembly, Participant
# Register your models here.

class ParticipantAdmin(admin.TabularInline):
    model = Participant
    extra = 3
    list_display = ['gender', 'count']


class AssemblyAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'date', 'closed']
    list_editable = ['closed']
    inlines = [
        ParticipantAdmin,
    ]
    def get_queryset(self, request):
        qs = super(AssemblyAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


admin.site.register(Assembly, AssemblyAdmin)
