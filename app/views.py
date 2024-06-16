import json
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, InvalidPage
from django.urls import reverse
from app.models import *
from django.contrib.auth import login, authenticate, logout
from app.forms import *
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.messages import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Count

# Create your views here.
QUESTIONS = list(Question.objects.annotate(likes_count=Count('questionlike')).all())
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
    if user.is_authenticated:
        profile = list(Profile.objects.filter(user=user))[0]
        return render(request, 'index.html', {
            'questions': paginate(QUESTIONS, request, 10), 
            'user': user,                    
            'profile': profile
            })
    return render(request, 'index.html', {
        'questions': paginate(QUESTIONS, request, 10), 
        'user': user
        }) 

@require_http_methods(['GET', 'POST'])
def loginView(request):
    if request.method == 'GET':
        loginForm = LoginForm()
    if request.method == 'POST':
        loginForm = LoginForm(data=request.POST)
        if loginForm.is_valid():
            user = authenticate(request, **loginForm.cleaned_data)
        if user:
            login(request, user)
            return redirect(reverse('index'))
        else:
            messages.add_message(request, ERROR, 'Authentication failed')
            return render(request, 'login.html', {'form': loginForm })
    return render(request, 'login.html', {'form': loginForm })

def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('index'))

def signup(request):
    if request.method == 'GET':
        registerForm = RegisterForm()
    if request.method == 'POST':
        registerForm = RegisterForm(data=request.POST, files=request.FILES)
        if registerForm.is_valid():
            user = registerForm.save()
            if user:
                return redirect(reverse('index'))
    
    return render(request, 'signup.html', {'form': registerForm })

def ask(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    profile = list(Profile.objects.filter(user=request.user))[0]
    if request.method == 'GET':
        questionForm = QuestionForm()
    if request.method == 'POST':
        questionForm = QuestionForm(data=request.POST)
        if questionForm.is_valid():
            question = Question(title=questionForm.cleaned_data["title"], text=questionForm.cleaned_data["text"], 
                                user=request.user)
            question.save()
            if question:
                question.user = request.user
                if profile:
                # return redirect(reverse('question', args=[question.id - 1]))
                    return render(request, 'question_detail.html', {
                            'question': question, 
                            'answersCount': 0,
                            'form': questionForm,
                            'profile': profile,
                            'user': request.user
                    })
                return render(request, 'question_detail.html', {
                            'question': question, 
                            'answersCount': 0,
                            'form': questionForm,
                            'user': request.user
                    }) 
            return redirect(reverse('index'))

    return render(request, 'ask.html', {'form': questionForm})

def hot(request):
    hot = Question.objects.get_hot()
    return render(request, 'hot.html', {'questions': paginate(hot, request, 10) })

def question(request, question_id):
    item = Question.objects.get(id=question_id)
    # item = QUESTIONS[question_id - 1]
    answers = list(Answer.objects.filter(question=item))
    profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        answerForm = AnswerForm()
    if request.method == 'POST':
        answerForm = AnswerForm(data=request.POST)
        if answerForm.is_valid():
            newAnswer = answerForm.save(commit=False)
            newAnswer.question = item
            newAnswer.user = request.user
            newAnswer.save()
        
    if profile:
        return render(request, 'question_detail.html', {
            'question': item, 
            'answersCount': len(answers),
            'answers': answers,
            'form': answerForm,
            'profile': profile
        })
    return render(request, 'question_detail.html', {
            'question': item, 
            'answersCount': len(answers),
            'answers': answers,
            'form': answerForm
        }) 

def settings(request):
    profile = list(Profile.objects.filter(user=request.user))[0]
    if request.method == 'POST':
        editUserForm = EditUserForm(data=request.POST, instance=request.user)
        editUserForm.actual_user = request.user
        editProfileForm = EditProfileForm(data=request.POST, files=request.FILES, instance=Profile.objects.get(user=request.user))
        # editUser = User()
        if editProfileForm.is_valid() and editUserForm.is_valid():
            editUserForm.save()
            editProfileForm.save()
            messages.success(request, 'Profile is updated')
            return redirect(reverse('settings'))
    else:
        editUserForm = EditUserForm(instance=request.user)
        editProfileForm = EditProfileForm(instance=Profile.objects.get(user=request.user))
    return render(request, 'settings.html', {
        'userform': editUserForm,
        'profileform': editProfileForm,
        'profile': profile
    })

def tag(request, tag_name):
    tag_questions = list(Question.objects.get_by_tag(tag_name))
    return render(request, 'tag.html', {'questions': paginate(tag_questions, request, 10), 'tag': tag_name })


@require_http_methods(["POST"])
@login_required(login_url="login")
@csrf_protect
def questionlike(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    profile, profile_created = Profile.objects.get_or_create(user=request.user)
    questionlike, questionlike_created = QuestionLike.objects.get_or_create(question=question, user=profile)
    if "dislikebutton" in request.POST:
        questionlike.delete()
    
    return redirect(reverse('index'))



@require_http_methods(["POST"])
@login_required(login_url="login")
@csrf_protect
def answerlike(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    profile, profile_created = Profile.objects.get_or_create(user=request.user)
    answerlike, answerlike_created = AnswerLike.objects.get_or_create(answer=answer, user=profile)
    if not answerlike_created:
        answerlike.delete()
    
    return redirect(reverse('index'))



# @login_required(login_url="login")
# @csrf_protect
# @require_http_methods(["POST"])
# def questionlike(request, question_id):
#     print(request.body)
#     body = json.loads(request.body)
#     question = get_object_or_404(Question, pk=question_id)
#     profile, profile_created = Profile.objects.get_or_create(user=request.user)
#     question_like, question_like_created = QuestionLike.objects.get_or_create(question=question, user=profile)

#     if not question_like_created:
#         question_like.delete()

#     body['likes_count'] = question_like.objects.filter(question=question).count()

#     return JsonResponse(body)



@login_required(login_url="login")
@csrf_protect
@require_http_methods(["POST"])
def questiondislike(request, question_id):
    body = json.loads(request.body)
    print(request.body)
    question = get_object_or_404(Question, pk=question_id)
    profile, profile_created = Profile.objects.get_or_create(user=request.user)
    question_like, question_like_created = QuestionLike.objects.get_or_create(question=question, user=profile)

    if not question_like_created:
        question_like.delete()

    body['dislikes_count'] = -question_like.objects.filter(question=question).count()

    return JsonResponse(body)

# def correctanswer(request):
