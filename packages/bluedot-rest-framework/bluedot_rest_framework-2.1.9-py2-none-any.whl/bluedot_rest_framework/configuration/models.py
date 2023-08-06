from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractConfiguration(AbstractRelationTime):

    configuration_type = models.IntegerField()
    title = models.CharField(max_length=255)
    value = models.JSONField()

    class Meta:
        abstract = True


class Configuration(AbstractRelationTime):

    class Meta:
        db_table = 'configuration'
