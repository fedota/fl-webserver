from django.shortcuts import render
from .models import Problem
from .kube import spawn_services

import zipfile

def start_problem(request, id):
    print("starting ", id)
    init_files_zip = Problem.objects.get(id=id).files

    with zipfile.ZipFile(init_files_zip, 'r') as zip_ref:
        zip_ref.extractall("data/{}".format(id))

    spawn_services(id)

def stop_problem(request, id):
    print("stopping ", id)