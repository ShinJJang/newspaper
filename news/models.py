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


class Vote(models.Model):
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(User)
    is_up = models.BooleanField("추천 또는 비추천")

    def __str__(self):
        result = self.user.username + " vote to thread id " + str(self.thread.id)
        if self.is_up:
            return result + " with +1"
        else:
            return result + " with -1"