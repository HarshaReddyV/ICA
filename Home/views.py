from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def Index(request):
    return render(request, 'Home/index.html')
