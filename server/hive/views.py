from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.base import ContentFile

import os

BASE_PATH = "files/"

def crack(request):
    if request.method == 'POST':
        save_file(request.FILES['h_file'])
        return HttpResponse("SAVED.")
    return HttpResponse("not post")

def save_file(f):
    try:
        os.mkdir(BASE_PATH)
    except:
        pass

    full_filename = os.path.join(BASE_PATH, f.name)
    file_content = ContentFile(f.read())

    fout = open(full_filename, 'wb+')
    for chunk in file_content.chunks():
        fout.write(chunk)
    fout.close()