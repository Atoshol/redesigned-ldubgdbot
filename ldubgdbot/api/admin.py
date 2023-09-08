from django.contrib import admin
from ldubgdbot.api.models import Student, Teacher, Admin, User, Group


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
admin.site.register(User)
admin.site.register(Group)
