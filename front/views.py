from django.shortcuts import render
from django.http import HttpResponse
from . import tts
import json


# Create your views here.
def index(request):
    if request.is_ajax():
        user_range = int(request.POST.get('range'))
        user_type = str(request.POST.get('question_type'))
        user_num = int(request.POST.get('num'))
        context = (tts.init_audio(user_range, user_type, user_num))
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        return render(request, "maths.html")

def yuwen(request):
    return render(request,"yuwen.html")

def english(request):
    return render(request,"english.html")