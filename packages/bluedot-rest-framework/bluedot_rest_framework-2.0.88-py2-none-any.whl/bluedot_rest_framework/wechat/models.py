from django.db import models


class WeChatUser(models.Model):
    openid = models.CharField(max_length=32)
    unionid = models.CharField(max_length=32)
    nick_name = models.CharField(max_length=100)
    gender = models.IntegerField()
    language = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    province = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    avatar_url = models.TextField()
    subscribe = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wechat_user'
