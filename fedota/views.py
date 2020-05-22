from django.shortcuts import render
from .models import Problem
from .kube import spawn_services

import zipfile

def start_problem(request, id):
    print("starting ", id)
    init_files_zip = Problem.objects.get(id=id).files

    # TODO: import viper 
    problem_dir = "{data-dir}/{problem-id}".format(data-dir=viper.GetString("DATA_DIR") problem-id=id)
    with zipfile.ZipFile(init_files_zip, 'r') as zip_ref:
        zip_ref.extractall(problem_dir)

    spawn_services(id)

def stop_problem(request, id):
    print("stopping ", id)