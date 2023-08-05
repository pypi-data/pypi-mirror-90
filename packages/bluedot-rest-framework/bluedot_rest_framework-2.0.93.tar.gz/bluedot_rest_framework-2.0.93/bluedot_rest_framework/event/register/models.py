from django.db import models


class AbstractEventRegister(models.Model):
    user_id = models.IntegerField(null=True)
    unionid = models.CharField(max_length=100, null=True)
    openid = models.CharField(max_length=100, null=True)
    wechat_id = models.IntegerField(null=True)
    event_id = models.CharField(max_length=32)
    event_type = models.IntegerField(default=1)
    source = models.IntegerField(default=0)
    state = models.IntegerField(default=0)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventRegister(AbstractEventRegister):
    class Meta:
        db_table = 'event_register'
