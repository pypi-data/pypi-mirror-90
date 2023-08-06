from django.db import models


class WeChatResponseMaterial(models.Model):
    user_name = models.CharField(max_length=32)
    material_type = models.IntegerField()
    title = models.CharField(max_length=255)
    remark = models.TextField()
    state = models.BooleanField(default=True)
    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wechat_response_material'


class WeChatResponseEvent(models.Model):
    material_id = models.IntegerField()
    user_name = models.CharField(max_length=32)
    event_type = models.IntegerField()
    title = models.CharField(max_length=255)
    event_key = models.CharField(max_length=100)
    text = models.CharField(max_length=255, null=True)
    remark = models.TextField()
    state = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wechat_response_event'


class WeChatQrcode(models.Model):
    openid = models.CharField(max_length=32)
    scene_str = models.CharField(max_length=32)
    ticket = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wechat_qrcode'
