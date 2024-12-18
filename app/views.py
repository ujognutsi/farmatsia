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

QUESTIONS = Question.objects.all().order_by('-created_at')
ANSWERS = list(Answer.objects.all())
most_common_tags = (
    Tag.objects.annotate(question_count=Count('question'))
    .order_by('-question_count')[:8]
)
tag_names = [tag.name for tag in most_common_tags]

users_with_counts = (
    User.objects.annotate(
        question_count=Count('question'),
        answer_count=Count('answer')
    ).annotate(total_count=Count('question') + Count('answer'))
    .order_by('-total_count')[:5]  # Получаем 5 пользователей с наибольшим количеством
)

def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page_obj = paginator.page(page_num)
    except InvalidPage:
        page_obj = paginator.page(1)
    return page_obj

def index(request):
    searchform = SearchForm()
    user = request.user
    if user.is_authenticated:
        profile = list(Profile.objects.filter(user=user))[0]
        return render(request, 'index.html', {
            'questions': paginate(QUESTIONS, request, 10), 
            'user': user,                    
            'profile': profile,
            'top_tags': tag_names,
            'top_users': users_with_counts,
            'searchform': searchform
            })
    return render(request, 'index.html', {
        'questions': paginate(QUESTIONS, request, 10), 
        'user': user,
        'top_tags': tag_names,
        'top_users': users_with_counts,
        'searchform': searchform
        }) 

@require_http_methods(['GET', 'POST'])
def loginView(request):
    searchform = SearchForm()
    if request.user.is_authenticated:
        return redirect(reverse('index'))
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
            return render(request, 'login.html', {'form': loginForm,
                                                  'top_tags': tag_names,
                                                  'top_users': users_with_counts,
                                                  'searchform': searchform })
    return render(request, 'login.html', {'form': loginForm,
                                          'top_tags': tag_names,
                                          'top_users': users_with_counts,
                                          'searchform': searchform 
                                           })

def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('index'))

def signup(request):
    searchform = SearchForm()
    if request.method == 'GET':
        registerForm = RegisterForm()
    if request.method == 'POST':
        registerForm = RegisterForm(data=request.POST, files=request.FILES)
        if registerForm.is_valid():
            user = registerForm.save()
            if user:
                return redirect(reverse('index'))
    
    return render(request, 'signup.html', {'form': registerForm,
                                           'top_tags': tag_names,
                                           'top_users': users_with_counts,
                                           'searchform': searchform })

def ask(request):
    searchform = SearchForm()
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    profile = list(Profile.objects.filter(user=request.user))[0]
    if request.method == 'GET':
        questionForm = QuestionForm()
    if request.method == 'POST':
        questionForm = QuestionForm(data=request.POST)
        if questionForm.is_valid():
            lastQuestionId = Question.objects.latest('id').id
            if not lastQuestionId:
                lastQuestionId = -1
            question = Question(id=lastQuestionId+1, title=questionForm.cleaned_data["title"], text=questionForm.cleaned_data["text"], 
                                user=request.user)
            question.save()
            tags_input = questionForm.cleaned_data['tagsInput']
            tags_list = [tag.strip() for tag in tags_input.split(',')]
            for tag_name in tags_list:
                lastTagId = Tag.objects.latest('id').id
                if not lastTagId:
                    lastTagId = -1
                tag, created = Tag.objects.get_or_create(id=lastTagId+1, name=tag_name)
                question.tags.add(tag)

            if question:
                question.user = request.user
                if profile:
                    return render(request, 'question_detail.html', {
                            'question': question, 
                            'answersCount': 0,
                            'form': questionForm,
                            'profile': profile,
                            'user': request.user,
                            'top_tags': tag_names,
                            'top_users': users_with_counts,
                            'searchform': searchform
                    })
                return render(request, 'question_detail.html', {
                            'question': question, 
                            'answersCount': 0,
                            'form': questionForm,
                            'user': request.user,
                            'top_tags': tag_names,
                            'top_users': users_with_counts,
                            'searchform': searchform
                    }) 
            return redirect(reverse('index'))

    return render(request, 'ask.html', {'form': questionForm,
                                        'top_tags': tag_names,
                                        'top_users': users_with_counts,
                                        'searchform': searchform })

def hot(request):
    searchform = SearchForm()
    hot = Question.objects.get_hot()
    return render(request, 'hot.html', {'questions': paginate(hot, request, 10),
                                        'top_tags': tag_names,
                                        'top_users': users_with_counts,
                                        'searchform': searchform })

def question(request, question_id):
    searchform = SearchForm()
    item = Question.objects.get(id=question_id)
    profile = Profile.objects.get(user=request.user.id)
    if request.method == 'GET':
        answerForm = AnswerForm()
    if request.method == 'POST':
        lastAnswerId = Answer.objects.latest('id').id
        if not lastAnswerId:
            lastAnswerId = -1
        answerForm = AnswerForm(data=request.POST)
        if answerForm.is_valid():
            newAnswer = Answer(id=lastAnswerId+1, text=answerForm.cleaned_data['text'], user=request.user,
            question=item)
            newAnswer.save()
        
    answers = list(Answer.objects.filter(question=item))
    if profile:
        return render(request, 'question_detail.html', {
            'question': item, 
            'answersCount': len(answers),
            'answers': answers,
            'form': answerForm,
            'profile': profile,
            'top_tags': tag_names,
            'top_users': users_with_counts,
            'searchform': searchform
        })
    return render(request, 'question_detail.html', {
            'question': item, 
            'answersCount': len(answers),
            'answers': answers,
            'form': answerForm,
            'top_tags': tag_names,
            'top_users': users_with_counts,
            'searchform': searchform
        }) 

def settings(request):
    searchform = SearchForm()
    profile = list(Profile.objects.filter(user=request.user))[0]
    if request.method == 'POST':
        editUserForm = EditUserForm(data=request.POST, instance=request.user)
        editUserForm.actual_user = request.user
        editProfileForm = EditProfileForm(data=request.POST, files=request.FILES, instance=Profile.objects.get(user=request.user))
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
        'profile': profile,
        'top_tags': tag_names,
        'top_users': users_with_counts,
        'searchform': searchform
    })

def tag(request, tag_name):
    searchform = SearchForm()
    profile = Profile.objects.get(user=request.user.id)
    tag_questions = list(Question.objects.get_by_tag(tag_name))
    if profile:
        return render(request, 'tag.html', {'questions': paginate(tag_questions, request, 10), 
                                            'tag': tag_name,
                                            'top_tags': tag_names,
                                            'top_users': users_with_counts,
                                            'profile': profile,
                                            'searchform': searchform })

    return render(request, 'tag.html', {'questions': paginate(tag_questions, request, 10), 
                                        'tag': tag_name,
                                        'top_tags': tag_names,
                                        'top_users': users_with_counts, 
                                        'searchform': searchform })

def search_view(request):
    searchform = SearchForm()
    questions = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            questions = Question.objects.filter(
                models.Q(title__icontains=query) | 
                models.Q(text__icontains=query)
            )
            paginate(questions, request, 10)
    
    return render(request, 'search.html', {'form': form, 
                                           'questions': questions,
                                           'top_tags': tag_names,
                                           'top_users': users_with_counts, 
                                           'searchform': searchform })

def vote_question(request, question_id, vote_type):
    searchform = SearchForm()
    if not request.user.is_authenticated:
        return redirect(reverse('login.html'))
    item = get_object_or_404(Question, id=question_id)
    answers = list(Answer.objects.filter(question=item))
    
    answerForm = AnswerForm()
    Vote.objects.filter(user=request.user, question=item).delete()
    profile = Profile.objects.get(user=request.user.id)
    
    Vote.objects.create(user=request.user, question=item, vote_type=vote_type)
    
    return render(request, 'question_detail.html', {
            'question': item, 
            'answersCount': len(answers),
            'answers': answers,
            'form': answerForm,
            'profile': profile,
            'top_tags': tag_names,
            'top_users': users_with_counts, 
            'searchform': searchform 
        })

@login_required
def vote_answer(request, answer_id, vote_type):
    answerForm = AnswerForm()
    item = Answer.objects.get(id=answer_id)
    profile = Profile.objects.get(user=request.user.id)
    answers = list(Answer.objects.filter(question=item.question))

    searchform = SearchForm()
    answer = get_object_or_404(Answer, id=answer_id)
    
    Vote.objects.filter(user=request.user, answer=answer).delete()

    Vote.objects.create(user=request.user, answer=answer, vote_type=vote_type)
    
    return render(request, 'question_detail.html', {
            'question': item, 
            'answersCount': len(answers),
            'answers': answers,
            'form': answerForm,
            'profile': profile,
            'top_tags': tag_names,
            'top_users': users_with_counts, 
            'searchform': searchform 
        })