from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from pip._vendor.requests import Response


class Index(View):

    def get(self, request):
        return HttpResponse('<h1>hello world</h1>')