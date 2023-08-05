from django.db import models


class EventComment(models.Model):

    user_id = models.IntegerField(null=True)
    unionid = models.CharField(max_length=100)
    openid = models.CharField(max_length=100)
    wechat_id = models.IntegerField(default=0)

    nick_name = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=255)
    schedule_id = models.IntegerField()
    event_id = models.IntegerField()
    state = models.IntegerField(default=0)
    data = models.TextField()

    like_count = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'event_comment'


class EventCommentLike(models.Model):
    user_id = models.CharField(max_length=100)
    unionid = models.CharField(max_length=100)
    openid = models.CharField(max_length=100)

    comment_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'event_comment_like'
