from django.test import TestCase
from .models import Question, Answer
from django.contrib.auth.models import User

class QuestionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.question = Question.objects.create(user=self.user, title='Sample Question', content='This is a test question.')

    def test_question_creation(self):
        self.assertEqual(self.question.title, 'Sample Question')
        self.assertEqual(self.question.content, 'This is a test question.')
        self.assertEqual(self.question.user.username, 'testuser')

class AnswerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.question = Question.objects.create(user=self.user, title='Sample Question', content='This is a test question.')
        self.answer = Answer.objects.create(user=self.user, question=self.question, content='This is a test answer.')

    def test_answer_creation(self):
        self.assertEqual(self.answer.content, 'This is a test answer.')
        self.assertEqual(self.answer.user.username, 'testuser')
        self.assertEqual(self.answer.question.title, 'Sample Question')