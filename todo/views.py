from django.shortcuts import render ,redirect
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
# Create your views here.

def main_page(request):
    if request.user.is_authenticated:
        today = datetime.now()
        todo_all=TodoTb.objects.filter(author_id=request.user.id).order_by('-type','finish_date','-create_date')
        todo_list=[]
        trash_list=[]
        late_list=[]
        notify_list=[]
        for todo in todo_all:
            if todo.finish_date==None and todo.flag==1:
                todo_list.append(todo)
            elif todo.flag==1 and todo.finish_date>=today:
                todo_list.append(todo)
            elif todo.flag==1 and todo.finish_date<today:
                late_list.append(todo)
                if todo.success==0:
                    notify_list.append(todo)
            elif todo.flag==0:
                trash_list.append(todo)

        return render(request, 'todo/main_page.html',
                      {'todo_list':todo_list ,'late_list':late_list,
                       'trash_list':trash_list,'notify_list':notify_list})
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

def todo_edit(request,pk):
    if request.method == 'POST':
        try:
            todo = TodoTb.objects.get(id=pk)
            if (todo.author_id==request.user.id and todo.flag == 1):
                if (request.POST['date'] == ''):
                    todo.title = request.POST['title']
                    todo.content = request.POST['content']
                    todo.type = request.POST['type']
                    todo.save()
                else :
                    todo.finish_date = request.POST['date']
                    todo.title = request.POST['title']
                    todo.content = request.POST['content']
                    todo.type = request.POST['type']
                    todo.save()
            else:
                pass
        except TodoTb.DoesNotExist:
            pass
        finally:
            return redirect('/')
    else:
        if request.user.is_authenticated:
            try:
                todo = TodoTb.objects.get(id=pk)
                if todo.author_id == request.user.id:
                    return render(request, 'todo/todo_edit.html', {'todo': todo})
                else:
                    return redirect('/')
            except TodoTb.DoesNotExist:
                return redirect('/')
        else:
            return redirect('/signin')

def todo_detail(request,pk):
    if request.user.is_authenticated:
        try:
            todo = TodoTb.objects.get(id=pk)
            if todo.author_id == request.user.id:
                return render(request, 'todo/todo_detail.html', {'todo': todo})
            else:
                return redirect('/')
        except TodoTb.DoesNotExist:
            return redirect('/')
    else:
        return redirect('/signin')

def todo_del(request,pk):
    if request.user.is_authenticated:
        try:
            todo=TodoTb.objects.get(id=pk)
            if todo.author_id == request.user.id:
                if (todo.flag == 0):
                    todo.delete()
                elif (todo.flag == 1):  # 1이 공개되있는거
                    todo.flag = 0
                    todo.save()
            else:
                pass
        except TodoTb.DoesNotExist:
            pass
        finally:
            return redirect('/')
    else:
        return redirect('/signin')

def todo_reload(request,pk):
    if request.user.is_authenticated:
        try:
            todo=TodoTb.objects.get(id=pk)
            if todo.author_id == request.user.id:
                if (todo.flag == 0):
                    todo.flag = 1
                    todo.save()
            else:
                pass
        except TodoTb.DoesNotExist:
            pass
        finally:
            return redirect('/')
    else:
        return redirect('/signin')

def todo_suc(request, pk):
    if request.user.is_authenticated:
        try:
            todo = TodoTb.objects.get(id=pk)
            if (todo.author_id == request.user.id and todo.flag == 1):
                if (todo.success== 0):
                    todo.success=1
                elif (todo.success == 1):  # 1이 공개되있는거
                    todo.success=0
                todo.save()
            else:
                pass
        except TodoTb.DoesNotExist:
            pass
        finally:
            return redirect('/')
    else:
        return redirect('/signin')

def todo_type(request, pk):
    if request.user.is_authenticated:
        try:
            todo = TodoTb.objects.get(id=pk)
            if todo.author_id == request.user.id and todo.flag == 1:
                if (todo.type== 0):
                    todo.type=1
                elif (todo.type == 1):  # 1이 공개되있는거
                    todo.type=0
                todo.save()
            else:
                pass
        except TodoTb.DoesNotExist:
            pass
        finally:
            return redirect('/')
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

def test(request):
    todo_all = TodoTb.objects.filter(author_id=request.user.id).order_by('-type', 'finish_date', '-create_date')
    return render(request,"todo/test.html",{'todo_list':todo_all})
