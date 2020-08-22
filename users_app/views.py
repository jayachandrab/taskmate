from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomRegisterForm
# Create your views here.
def register(request):
    context={}
    if request.method=="POST":
        register_form=CustomRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,("New User account Created. Login to get Started"))
            return redirect('register')
        else:
            context['register_form']=register_form

    else:
        register_form=CustomRegisterForm()
        context['register_form']=register_form
    return render(request,"register.html", context)