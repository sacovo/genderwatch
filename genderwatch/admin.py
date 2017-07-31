from django.contrib import admin
from genderwatch.models import Assembly
# Register your models here.


class AssemblyAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'date', 'closed']
    list_editable = ['closed']
    def get_queryset(self, request):
        qs = super(AssemblyAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


admin.site.register(Assembly, AssemblyAdmin)
