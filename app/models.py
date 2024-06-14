from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db.models.functions import Coalesce
from datetime import date

# Create your models here.
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
        # SELECT question FROM questionlikes WHERE 
        # return self.annotate(likes=Coalesce(models.Sum('questionlike'), 0)).order_by('-likes')
        # q = self.get().id
        # return self.order_by(Answer.objects.filter(question=q).count).reverse()[0:10]


        # вывести вопросы сортировкой по убыванию суммы questionlike с question == id
        # SELECT * FROM question ORDER BY COUNT(SELECT * FROM questionlike WHERE question == id)
        pass

    def get_new(self):
        return self.filter(created_at__day=date.today())

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=65535)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
#    vr = models.CharField(max_length=12)

    def __str__(self):
        return self.title

class ProfileManager(models.Manager):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=False, blank=True)

    def __str__(self):
        return self.user.username

class QuestionLikeManager(models.Manager):
    pass

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # unique_together = [
    #     ['question', 'user']
    # ]
    constraints = [
        models.UniqueConstraint(fields=['question', 'user'], name='unique like')
    ]

    def __str__(self):
        return str(self.question_id)

class AnswerLikeManager(models.Manager):
    pass

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    unique_together = [
        ['answer', 'user']
    ]

    def __str__(self):
        return self.answer_id
    
# class CustomUser(User):
#     avatar = models.ImageField()