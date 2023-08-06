from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractConfigs(AbstractRelationTime):

    configs_type = models.IntegerField()
    title = models.CharField(max_length=255)
    value = models.JSONField()

    class Meta:
        abstract = True


class Configs(AbstractRelationTime):

    class Meta:
        db_table = 'configs'
