from django.contrib import admin
from .models import Job, RequiredSkill, Job_Responsibilities, Job_Experience, SaveJob, Application, ApplicationStatus, Conversation, Message, JobFair, JobFairRegistration

# Register your models here.
admin.site.register(Job)
admin.site.register(RequiredSkill)
admin.site.register(Job_Responsibilities)
admin.site.register(Job_Experience)

admin.site.register(SaveJob)

admin.site.register(Application)
admin.site.register(ApplicationStatus)
admin.site.register(Conversation)
admin.site.register(Message)

admin.site.register(JobFair)
admin.site.register(JobFairRegistration)