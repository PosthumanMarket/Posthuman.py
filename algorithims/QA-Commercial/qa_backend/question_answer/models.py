from django.db import models
from django.contrib.auth.models import User


class DateTimeBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering = ("-created_at",)

class UserAnswer(DateTimeBase):
    question = models.CharField(max_length=255)
    answers = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)