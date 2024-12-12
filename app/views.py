from django.http import Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, InvalidPage
from django.urls import reverse
from app.models import *
from django.contrib.auth import *
from app.forms import *
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.messages import *


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
    user = request.user
    if not user:
        user = null
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, request, 10), 'user': user })

@require_http_methods(['GET', 'POST'])
def loginview(request):
    flag = False
    if request.method == 'GET':
        loginForm = LoginForm()
    if request.method == 'POST':
        loginForm = LoginForm(data=request.POST)
        if loginForm.is_valid():
            user = authenticate(request, **loginForm.cleaned_data)
        if user:
            flag = True
            login(request, user)
            return redirect(reverse('index'))
        else:
            messages.add_message(request, ERROR, 'Authentication failed')
            return render(request, 'login.html', {'form': loginForm })
    return render(request, 'login.html', {'form': loginForm })
    #return render(request, 'signup.html', {'form': loginForm})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('index'))

def signup(request):
    if request.method == 'GET':
        registerForm = RegisterForm()
    if request.method == 'POST':
        registerForm = RegisterForm(data=request.POST)
        if registerForm.is_valid():
            user = registerForm.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
    
    return render(request, 'signup.html', {'form': registerForm })

def ask(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            questionForm = QuestionForm()
        else:
            return redirect(reverse(f'login'))
    if request.method == 'POST':
        questionForm = QuestionForm(data=request.POST)
        if questionForm.is_valid():
            question = questionForm.save()
            if question:
                return redirect(reverse(f'question/{question.id}'))
            
    return render(request, 'ask.html', {'form': questionForm })

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
    if request.method == 'POST':
        editForm = EditProfileForm(data=request.POST)
        if editForm.is_valid():
            user = editForm.save()
            if user:
                return redirect(reverse('index'))
            
    return render(request, 'settings.html')

def tag(request, tag_name):
    tag_questions = list(Question.objects.get_by_tag(tag_name))
    return render(request, 'tag.html', {'questions': paginate(tag_questions, request, 10), 'tag': tag_name })
