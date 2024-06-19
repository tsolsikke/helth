from django.shortcuts import render
from django.http import HttpResponse


def list_diary(request):
    return HttpResponse('Hello, world!')
