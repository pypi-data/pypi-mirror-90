from django.db import models
from .abstract_models import AbstractQuestion, AbstractQuestionUser


class Question(AbstractQuestion):

    title = models.CharField(max_length=100)
    integral = models.IntegerField(default=0)
    qa = models.JSONField()

    class Meta:
        db_table = 'question'


class QuestionUser(AbstractQuestionUser):
    qa_id = models.IntegerField()

    title = models.CharField(max_length=100)
    integral = models.IntegerField(default=0)

    qa = models.JSONField()

    class Meta:
        db_table = 'question_user'
