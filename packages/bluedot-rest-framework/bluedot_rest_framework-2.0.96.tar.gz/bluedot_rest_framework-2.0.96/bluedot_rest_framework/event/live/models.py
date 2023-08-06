from django.db import models


class AbstractEventLivePPT(models.Model):
    event_id = models.IntegerField()

    user_id = models.IntegerField(null=True)
    unionid = models.CharField(max_length=32, null=True)
    openid = models.CharField(max_length=32, null=True)

    nick_name = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=255)

    state = models.IntegerField(default=0)
    data = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventLivePPT(AbstractEventLivePPT):
    image_list = models.JSONField(null=True)

    class Meta:
        db_table = 'event_live_ppt'
