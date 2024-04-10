from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class TagManager(models.Manager):
    pass

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def get_by_tag(self, Tag):
        return self.filter(Tag in self.tags)
    
    # def get_hot(self):
    #     return self.filter(self.id == question_id )


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=65535)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title

class AnswerManager(models.Manager):
    pass

class Answer(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=65535)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProfileManager(models.Manager):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class QuestionLikeManager(models.Manager):
    pass

class QuestionLike(models.Model):
    question_id = models.ManyToOneRel(Question, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    unique_together = [
        ['question_id', 'user_id']
    ]

    def __str__(self):
        return self.question_id

class AnswerLikeManager(models.Manager):
    pass

class AnswerLike(models.Model):
    answer_id = models.OneToOneField(Answer, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    unique_together = [
        ['answer_id', 'user_id']
    ]

    def __str__(self):
        return self.answer_id
    

# вывести вопросы сортировкой по убыванию суммы questionlike с question_id == id
# SELECT * FROM question ORDER BY COUNT(SELECT * FROM questionlike WHERE questiion_id == id)