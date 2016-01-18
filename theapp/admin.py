from django.contrib import admin

# Register your models here.

from theapp.models import User, City, EmailVerification, Notification
from theapp.models import Approval


class UserAdmin(admin.ModelAdmin):
    pass


class CityAdmin(admin.ModelAdmin):
    pass


class ApprovalAdmin(admin.ModelAdmin):
    pass


class EmailVerificationAdmin(admin.ModelAdmin):
    pass


class NotificationAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Approval, ApprovalAdmin)
admin.site.register(EmailVerification, EmailVerificationAdmin)
admin.site.register(Notification, NotificationAdmin)
