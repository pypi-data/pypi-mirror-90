from django.db import models


class WeChatQrcode(models.Model):
    user_name = models.CharField(max_length=32)
    param = models.JSONField()
    url = models.CharField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wechat_qrcode'


class WeChatQrcodeLogin(models.Model):
    unionid = models.CharField(max_length=100)
    code = models.IntegerField()
    url = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wechat_qrcode_login'
