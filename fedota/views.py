from django.shortcuts import redirect
from django.contrib import messages
from .models import Problem
from .kube import spawn_services

import zipfile

def start_problem(request, id):
    print("starting ", id)
    init_files_zip = Problem.objects.get(id=id).files

    # TODO: import viper 
    # problem_dir = "{data-dir}/{problem-id}".format(data-dir=viper.GetString("DATA_DIR") problem-id=id)
    # with zipfile.ZipFile(init_files_zip, 'r') as zip_ref:
    #     zip_ref.extractall(problem_dir)

    # TODO: Display appropriate message based on successfull completion of spawn_services
    spawn_services(id)
    messages.success(request, 'Spawing services for problem id %d' % id)
    return redirect('/fedota/problem')


def stop_problem(request, id):
    print("stopping ", id)
    messages.error(request, 'To be Implemented')
    return redirect('/fedota/problem')