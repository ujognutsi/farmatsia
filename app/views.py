from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
QUESTIONS = []
for i in range(1,40):
    QUESTIONS.append({
        'title': 'title' + str(i), 
        'id': i, 
        'text': 'text' + str(i)
    })

def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    page_obj = paginator.page(page_num)
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
    hot = QUESTIONS[5:20]
    return render(request, 'hot.html', {'questions': paginate(hot, request, 10) })

def question(request, question_id):
    item = QUESTIONS[question_id - 1]
    return render(request, 'question_detail.html', {'question': item })