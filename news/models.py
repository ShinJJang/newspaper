from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    title = models.CharField("제목", max_length=30)
    url = models.CharField("URL", max_length=255)
    content = models.TextField("내용")
    writer = models.ForeignKey(User)
    pub_date = models.DateTimeField("작성 시간", auto_now_add=True)

    def __str__(self):
        return self.title