from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    context={"welcome_message":"Welcome to index page"}
    return render(request,'index.html',context)

@login_required
def todolist(request):
    if request.method=="POST":
        print("===========")
        form=TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).manager=request.user
            form.save()

            messages.success(request,("New Task Added!"))
            return redirect('todolist')
    else:
        
        context={"welcome_message":"Welcome to todolist page"}
        all_tasks=TaskList.objects.filter(manager=request.user)
        paginator=Paginator(all_tasks,5)       
        page=request.GET.get('page')
        all_tasks=paginator.get_page(page)
        context['all_tasks']=all_tasks
        return render(request,'todolist.html',context)
    
def about(request):
    context={"welcome_message":"Welcome to about page"}
    return render(request,'about.html',context)

def contact(request):
    context={"welcome_message":"Welcome to contact page"}
    return render(request,'contact.html',context)
   
@login_required
def delete_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    if task.manager==request.user:
        task.delete()
    else:
        messages.error(request,("Access Denied"))
    return redirect('todolist')

@login_required
def edit_task(request,task_id):
    if request.method=="POST":
        task_obj=TaskList.objects.get(pk=task_id)
        form=TaskForm(request.POST or None,instance=task_obj)
        if form.is_valid():
            form.save()
        messages.success(request,("Task Edited!"))
        return redirect('todolist')
    else:
        task_obj=TaskList.objects.get(pk=task_id)

        return render(request,'edit.html',{"task_obj":task_obj})
@login_required  
def complete_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    if task.manager==request.user:

        task.done=True
        task.save()
    else:
        messages.error(request,("Access Denied"))
    return redirect('todolist')
@login_required
def pending_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    task.done=False
    task.save()
    return redirect('todolist')


    