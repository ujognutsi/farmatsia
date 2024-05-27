from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage
from app.models import *

# Create your views here.
QUESTIONS = list(Question.objects.all())
ANSWERS = list(Answer.objects.all())

def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page_obj = paginator.page(page_num)
    except InvalidPage:
        page_obj = paginator.page(1)
    return page_obj

def index(request):
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, request, 10) })

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')

def hot(request):
    hot = Question.objects.get_hot()
    return render(request, 'hot.html', {'questions': paginate(hot, request, 10) })

def question(request, question_id):
    item = QUESTIONS[question_id]
    answers = list(Answer.objects.filter(question=item))
    return render(request, 'question_detail.html', {
        'question': item, 
        'answersCount': len(answers),
        'answers': answers
    })

def settings(request):
    return render(request, 'settings.html')

def tag(request, tag_name):
    tag_questions = list(Question.objects.get_by_tag(tag_name))
    return render(request, 'tag.html', {'questions': paginate(tag_questions, request, 10), 'tag': tag_name })