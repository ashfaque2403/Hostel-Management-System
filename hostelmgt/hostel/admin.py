from django.utils import timezone
from django.contrib import admin
from django.db.utils import IntegrityError
from .models import Room,UserProfile,Complaint,RoomAllotment,LeaveRequest,Attendance,Fees
# Register your models here.
admin.site.register(Room)
admin.site.register(UserProfile)
admin.site.register(Complaint)
admin.site.register(RoomAllotment)
admin.site.register(LeaveRequest)

admin.site.register(Attendance)


class FeesAdmin(admin.ModelAdmin):
    exclude = ('attendance',)  # Specify the field(s) you want to exclude

admin.site.register(Fees, FeesAdmin)