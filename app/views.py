from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
questions = []
for i in range(1,40):
    questions.append({
        'title': 'title' + str(i), 
        'id': i, 
        'text': 'text' + str(i)
    })

def index(request):
    return render(request, 'index.html', {'question': questions})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')