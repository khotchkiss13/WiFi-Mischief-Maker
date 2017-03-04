from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.base import ContentFile

from password import crack_password

import os
import getpass

HCCAP_FILENAME = 'hashcat.hccap'
HIVE_BLACKLIST = [4]

def crack(request):
    if request.method == 'POST':
        f = request.FILES['h_file']
        file_content = ContentFile(f.read())

        home = os.path.expanduser("~")
        full_filename = os.path.join(home, HCCAP_FILENAME)

        # saves file
        fout = open(full_filename, 'wb+')
        for chunk in file_content.chunks():
            fout.write(chunk)
        fout.close()

        password = crack_password(HCCAP_FILENAME, HIVE_BLACKLIST)

        # deletes hccap file
        os.system('rm ' + full_filename)

        return HttpResponse(password)
    return HttpResponse("not post")

