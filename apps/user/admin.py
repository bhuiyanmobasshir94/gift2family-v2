from django.contrib import admin

from .models import User, AgentProfile, AgentInterestRate


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('password',)


admin.site.register(User, UserAdmin)
admin.site.register(AgentProfile)
admin.site.register(AgentInterestRate)


