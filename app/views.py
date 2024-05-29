from django.http import Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, InvalidPage
from django.urls import reverse
from app.models import *
from django.contrib.auth import *
from app.forms import *
from django.views.decorators.http import require_http_methods


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

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        loginForm = LoginForm()
    if request.method == 'POST':
        loginForm = LoginForm(data=request.POST)
        if loginForm.is_valid():
            user = authenticate(request, **loginForm.cleaned_data())
        if user:
            return redirect(reverse('signup'))
    return render(request, 'login.html', {'form': loginForm })

def log_out(request):
    logout(request)
    return redirect(reverse('index'))

def signup(request):
    # допилить
    if request.method == 'GET':
        registerForm = RegisterForm()
    if request.method == 'POST':
        registerForm = RegisterForm(data=request.POST)
        if registerForm.is_valid():
            user = registerForm.save()
            if user:
                return redirect(reverse('index'))
            else:
                registerForm.add_error(field=None, error="User saving error!")
    
    return render(request, 'signup.html', {'form': registerForm })

def ask(request):
    return render(request, 'ask.html')

def hot(request):
    hot = Question.objects.get_hot()
    return render(request, 'hot.html', {'questions': paginate(hot, request, 10) })

def question(request, question_id):
    # на индексе не отображается количество вопросов
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