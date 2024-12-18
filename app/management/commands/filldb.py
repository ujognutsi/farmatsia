from django.core.management.base import BaseCommand, CommandError
from app.models import Profile, Question, Answer, Tag, User
import random
from django.db import *

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int) 
    
    def handle(self, *args, **options):
        ratio = options["ratio"]
        users = []
        profiles = []
        for i in range(ratio):
            users.append(User(id=i, username=f"User #{i}", password=f"Password{i}{i%1000}"))
            profiles.append(Profile(id=i, user=users[i]))
        
        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)
        print("Users and profiles added")
        tags = []
        for i in range(ratio):
            tags.append(Tag(id=i, name=f"Tag #{i}"))
        
        Tag.objects.bulk_create(tags)
        print("Tags added")
        questions = []
        for i in range(ratio * 10):
            randomId = random.randint(0, ratio - 1)
            # print(User.objects.get(id=randomId))
            questions.append(Question(id=i, title=f"Question #{i}", text=f"Question text #{i}",
                                      user=User.objects.get(id=randomId)))
        
        Question.objects.bulk_create(questions)

        for i in range(ratio * 10):
            questions[i].tags.add(*random.sample(tags, random.randint(1, 5)))

        print("Questions added")
        answers = []

        for i in range(ratio * 100):
            answers.append(Answer(id=i, text=f"Answer #{i} text", 
                                  question=Question.objects.get(id=random.randint(0, ratio * 10 - 1)),
                                  user=User.objects.get(id=random.randint(0, ratio - 1))))

        Answer.objects.bulk_create(answers)
        print("Answers added")
        print("The base is filled")