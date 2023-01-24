from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, File, Schema
from ninja.files import UploadedFile
from ninja.security import django_auth
from django.http import JsonResponse, HttpResponse
from .models import ChessELO, ChessNotation, ChessNoationCheckPoint
import pandas as pd
from api.spark.processor import Processor
from django.core import serializers

api = NinjaAPI(csrf=True)


@api.post('/uploadfile', auth=django_auth)
def uploadfile(request, uploaded_file: UploadedFile = File(...)):
  # UploadedFile is an alias to Django's UploadFile
    with open(f'api\\dist\\notation\\{uploaded_file.name}', 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return uploaded_file.name


@api.get('/parse', auth=django_auth)
def parse_notation(request, filename: str, num: int):
    try:
        k = ChessNoationCheckPoint.objects.get(fname=filename[:-4])
        print(k.checkpoint, k.fname)
        msg = Processor(
            f'api\\dist\\notation\\{filename}', num, checkpoint=k.checkpoint, name=k.fname)
        print('done')
    except:
        print(filename[:-4])
        msg = Processor(
            f'api\\dist\\notation\\{filename}', num, checkpoint=None, name=filename[:-4])

    return


@api.get('/getdata', auth=django_auth)
def get_data(request):
    data = ChessNotation.objects.all()
    data_json = serializers.serialize('json', data)
    return HttpResponse(data_json, content_type="text/json-comment-filtered")


urlpatterns = [
    path('api/', api.urls)
]
