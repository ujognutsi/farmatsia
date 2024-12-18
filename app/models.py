from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db.models.functions import Coalesce
from datetime import date

class TagManager(models.Manager):
    pass

class Tag(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def get_by_tag(self, Tag):
        return self.filter(tags__name__icontains=Tag)

    def get_hot(self):
        pass

    def get_new(self):
        return self.filter(created_at__day=date.today())

class Question(models.Model):
    class Meta:
        ordering = ['created_at']
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=65535)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    @property
    def likes(self):
        return self.vote_set.filter(vote_type='like').count()

    @property
    def dislikes(self):
        return self.vote_set.filter(vote_type='dislike').count()

class AnswerManager(models.Manager):
    pass

class Answer(models.Model):
    text = models.CharField(max_length=65535)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['created_at']

    @property
    def likes(self):
        return self.vote_set.filter(vote_type='like').count()

    @property
    def dislikes(self):
        return self.vote_set.filter(vote_type='dislike').count()

class ProfileManager(models.Manager):
    pass

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=False, blank=True, upload_to="uploads")

    def __str__(self):
        return self.user.username

class Vote(models.Model):
    VOTE_TYPE_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=7, choices=VOTE_TYPE_CHOICES)

    class Meta:
        unique_together = ('user', 'question')
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"{self.user} - {self.vote_type} on {self.question or self.answer}"
