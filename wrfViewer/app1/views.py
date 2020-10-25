"""_"""
import json

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from app1.parser import rslOutParser

# Create your views here.

class tryClass(View):
    """_"""
    def get(self, request):
        """ GET Request时执行的方法 """
        rslFilePath = '/Users/richard/Documents/iOS_Study/swift_program/WRFViewer/resources/djangoResources/rsl.out.0000.log'
        rslParser = rslOutParser(rslFilePath)
        
        print('start to parse')

        if request.GET.get('fromRowIndex'):
            try:
                fromRowIndex = int(request.GET.get('fromRowIndex'))
            except ValueError:
                fromRowIndex = 0
        else:
            fromRowIndex = 0

        outData = rslParser.tryParse(fromRowIndex)
        outJson = json.dumps(outData)
        return HttpResponse(outJson)

def index(request):
    """ 测试函数 """
    return HttpResponse('Hello world')
