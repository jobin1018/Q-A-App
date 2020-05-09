from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse

# Create your models here.


class Questions(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=False)
    created_date = models.DateTimeField(default=now, editable=False)
    asker = models.ForeignKey(User, on_delete=models.CASCADE)
    qst_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Questions"

    def get_absolute_url(self):
        return reverse("questions-detail", kwargs={"pk": self.pk})


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=False)
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    replied_date = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name_plural = "Answers"
