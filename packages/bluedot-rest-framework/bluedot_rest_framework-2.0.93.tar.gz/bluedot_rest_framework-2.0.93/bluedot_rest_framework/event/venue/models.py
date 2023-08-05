from django.db import models


class EventVenue(models.Model):
    event_id = models.IntegerField()
    image_list=models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'event_venue'