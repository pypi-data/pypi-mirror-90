from django.db import models


class AbstractUser(models.Model):
    wechat_id = models.IntegerField(null=True)
    unionid = models.CharField(max_length=100, null=True)
    openid = models.CharField(max_length=100, null=True)

    user_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    tel = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=100, null=True)
    job = models.CharField(max_length=100, null=True)

    country = models.CharField(max_length=100, null=True)
    source_type = models.CharField(max_length=100, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):

    class Meta:
        db_table = 'user'
        swappable = 'FORNTEND_USER_MODEL'
