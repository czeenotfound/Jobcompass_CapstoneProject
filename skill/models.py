from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_validated = models.BooleanField(default=False)  # To track if it's from skills.txt
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name