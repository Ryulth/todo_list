from django.shortcuts import render ,redirect
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
import datetime
# Create your views here.

def main_page(request):
    if request.user.is_authenticated:
        todo_list=TodoTb.objects.filter(author_id=request.user.id).order_by('-type','finish_date','-create_date')

        return render(request, 'todo/main_page.html',{'todo_list':todo_list})
    else:
        return redirect('/signin')

def todo_reg(request):
    if request.method == 'POST':
        print(request.POST)
        if(request.POST['date']==''):
            new_todo = TodoTb(title=request.POST['title'], content=request.POST['content'],
                               type=request.POST['type'], author_id=request.user.id)
        else :
            new_todo=TodoTb(title=request.POST['title'],content=request.POST['content'],
                        finish_date=request.POST['date'],type=request.POST['type'],author_id=request.user.id)

        new_todo.save()
        return redirect('/todo_reg')
    else:
        if request.user.is_authenticated:
            return render(request, 'todo/todo_reg.html')
        else:
            return redirect('/signin')


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        id=request.POST['username']
        pw=request.POST['password']
        user=authenticate(username=id,password=pw)
        if user is not None:
            login(request,user)
            return redirect('/')
        else :
            return redirect('/signin')
    else:
        form = LoginForm()
        return render(request, 'todo/login.html', {'form':form})

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/')
    else:
        form = UserForm()
        return render(request, 'todo/login.html', {'form': form})