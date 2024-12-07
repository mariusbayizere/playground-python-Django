from django.shortcuts import render
from django.http import HttpResponse


def say_hello(request): 
    return render(request, 'hello.html', { "name" : "Bayizere marius ", "Postion" : 'His is software Engineering SAND Teachinology'})

