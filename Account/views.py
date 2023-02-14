from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from django.http import HttpResponse

class Registration(generics.GenericAPIView):
    def get(self,request):
        
        return HttpResponse("kamal")
    