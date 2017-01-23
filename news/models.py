from django.db import models
from django.contrib.auth.models import User
from news.util.ranking import hot


class Thread(models.Model):
    title = models.CharField("제목", max_length=255)
    url = models.CharField("URL", max_length=255)
    content = models.TextField("내용")
    writer = models.ForeignKey(User)
    pub_date = models.DateTimeField("작성 시간", auto_now_add=True)

    def __str__(self):
        return self.title

    def get_vote_count(self):
        """This function is intended to return count of voted on thread.

        :return: The sum of vote, upvote - devote
        """
        vote_count = self.vote_set.filter(is_up=True).count() - self.vote_set.filter(is_up=False).count()
        if vote_count >= 0:
            return "+ " + str(vote_count)
        else:
            return "- " + str(abs(vote_count))

    def get_score(self):
        """ This function is intended to return score calculated by hot ranking algorithm from reddit.
        Check out URL containing detail of hot ranking algorithm in news.util.ranking.py

        :return: The score calculated by hot ranking algorithm
        """
        upvote_count = self.vote_set.filter(is_up=True).count()
        devote_count = self.vote_set.filter(is_up=False).count()
        return hot(upvote_count, devote_count, self.pub_date.replace(tzinfo=None))


class Vote(models.Model):
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(User)
    is_up = models.BooleanField("추천 여부", default=True)

    def __str__(self):
        result = self.user.username + " vote to thread id " + str(self.thread.id)
        if self.is_up:
            return result + " with +1"
        else:
            return result + " with -1"


class Comment(models.Model):
    thread = models.ForeignKey(Thread)
    writer = models.ForeignKey(User)
    parent_comment = models.ForeignKey("self", null=True, blank=True)
    content = models.TextField("내용")
    pub_date = models.DateTimeField("작성 일자", auto_now_add=True)

    def __str__(self):
        return self.writer.username + ": " + self.content
