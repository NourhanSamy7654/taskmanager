from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from .models import Task
from .form import taskform
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    form=UserCreationForm(request.POST or None)
    if form.is_valid():
        user=form.save()
        print(user)
        login(request,user)
        return redirect('tasks:task_list')
    return render(request,'tasks/register.html',{'form':form})

@login_required
def task_list(request):
    if request.user.is_staff:
        tasks=Task.objects.all().order_by('-created_at')
    else:
     tasks=Task.objects.filter(owner=request.user).order_by('-created_at')
    # tasks=Task.objects.all().order_by('-created_at')
    context={
        'tasks': tasks,
        'total':tasks.count(),
        'pending':tasks.filter(status='pending').count(),
        'in_progress': tasks.filter(status='in_progress').count()
        
    }
    return render(request,'tasks/task_list.html',context)
def task_details(request,pk):
    #when using get you must use try-except because get fetch one element and get
    #  only unquie value when find mulite value match returen error 
    # try:
    #     tasks = Task.objects.get(pk=pk)

    # except Task.DoesNotExist:
    #     raise Http404("Task not found")
    tasks=get_object_or_404(Task,pk=pk,owner=request.user)
    return render(request,'tasks/task_details.html',{'tasks':tasks})
@login_required
def create_task(request):
    form=taskform(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.owner = request.user 
        form.save()
        messages.success(request,"created secess!")
        return  redirect('tasks:task_list')
    return render(request,'tasks/task_form.html',{'form':form, 'action': 'create'})
@login_required
def update_task(request,pk):
    task=get_object_or_404(Task,pk=pk,owner=request.user)
    form=taskform(request.POST or None,instance=task)
    if form.is_valid():
      
        form.save()
        messages.success(request,"updated success!")
        return redirect('tasks:tasks_details', pk=task.pk)
    return render(request,'tasks/task_form.html',{'form':form, 'action': 'Update'})
@login_required
def delete_task(request,pk):
    task=get_object_or_404(Task,pk=pk)
    if request.method=='POST':
        task.delete()
        messages.success(request,"success delete!")
        return  redirect('tasks:task_list')
    return render(request,'tasks/confirm_delete.html',{'task':task})

     


