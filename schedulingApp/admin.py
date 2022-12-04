from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(CourseToAssignedTAEntry)
admin.site.register(CourseToProfessorEntry)
admin.site.register(LabSection)
