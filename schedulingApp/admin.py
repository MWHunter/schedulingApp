from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Section)
admin.site.register(CourseToAssignmentEntry)
admin.site.register(CourseToAssignedUserEntry)
admin.site.register(SectionToAssignedUserEntry)
admin.site.register(SectionToAssignmentEntry)
