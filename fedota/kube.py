from os import path

import yaml
import os
from django.conf import settings

from kubernetes import client, config

def create_namespace(name):
    body = client.V1Namespace()
    body.metadata = client.V1ObjectMeta(name=name)
    core_v1 = client.CoreV1Api()
    resp = core_v1.create_namespace(body=body)
    print("Namespace created. status='%s'" % resp.metadata.name)

def delete_namespace(name):
    core_v1 = client.CoreV1Api()
    resp = core_v1.delete_namespace(name=name, body=client.V1DeleteOptions())
    print("Namespace deleted. status='%s'" % resp.metadata.name)


def spawn_services(id):
    config.load_kube_config()

    core_v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    # create the namespace as the fl problem id
    if str(id) in core_v1.list_namespace().items 
        delete_namespace(str(id))
    create_namespace(str(id))

    # create a fl pv for each problem
    pv_config_file = os.path.join(
        settings.BASE_DIR, "k8s/fl-pv.yaml")
    with open(deployment_config_file) as f:
        dep = yaml.safe_load_all(f)
        dep['metadata'].name = str(id)
        dep['spec'].hostPath.path = os.path.join(
        settings.BASE_DIR, str(id))
        resp = core_v1.create_persistent_volume(body=dep)
        print("FL PV created. status='%s'" % resp.metadata.name)

    # create fl coordinator service and deployment
    pvc_config_file = os.path.join(
        settings.BASE_DIR, "k8s/fl-pvc.yaml")
    with open(deployment_config_file) as f:
        dep = yaml.safe_load_all(f)
        resp = core_v1.create_namespaced_persistent_volume_claim(
            namespace=id, body=dep)
        print("FL PVC created. status='%s'" % resp.metadata.name)

    # create fl coordinator service and deployment
    deployment_config_file = os.path.join(
        settings.BASE_DIR, "k8s/fl-coordinator.yaml")
    with open(deployment_config_file) as f:
        dep = yaml.safe_load_all(f)

        for i in dep:
            print(i['kind'])
            if i['kind'] == 'Service':
                resp = core_v1.create_namespaced_service(
                    namespace=id, body=i)
                print("FL Coorinator Service created. status='%s'" % resp.metadata.name)

            elif i['kind'] == 'Deployment':
                resp = apps_v1.create_namespaced_deployment(
                    namespace=id, body=i)
                print("FL Coordinator Deployment created. status='%s'" % resp.metadata.name)

    # create fl selector service and deployment
    deployment_config_file = os.path.join(
        settings.BASE_DIR, "k8s/fl-selector.yaml")
    with open(deployment_config_file) as f:
        dep = yaml.safe_load_all(f)

        for i in dep:
            print(i['kind'])
            if i['kind'] == 'Service':
                resp = core_v1.create_namespaced_service(
                    namespace=id, body=i)
                print("FL Selector Service created. status='%s'" % resp.metadata.name)

            elif i['kind'] == 'Deployment':
                resp = apps_v1.create_namespaced_deployment(
                    namespace=id, body=i)
                print("FL Selector Deployment created. status='%s'" % resp.metadata.name)