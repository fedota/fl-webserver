from os import path

import yaml
import os
from django.conf import settings

from kubernetes import client, config
from kubernetes.client.rest import ApiException

def create_namespace(name):
    body = client.V1Namespace()
    body.metadata = client.V1ObjectMeta(name=name)
    core_v1 = client.CoreV1Api()
    resp = core_v1.create_namespace(body=body)
    print("Namespace created. status='%s'" % resp)

def delete_namespace(name):
    core_v1 = client.CoreV1Api()
    try:
        resp = core_v1.delete_namespace(name=name, body=client.V1DeleteOptions())
        print("Namespace deleted. status='%s'" % resp)
    except ApiException:
        print("Namespace not found")

def create_service_deployment(id, service_name, deployment_config_file):
    core_v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    # create fl coordinator/selector service and deployment
    with open(deployment_config_file) as f:
        dep = yaml.safe_load_all(f)

        for yaml_object in dep:
            print(yaml_object['kind'])
            if yaml_object['kind'] == 'Service':
                try:
                    resp = core_v1.create_namespaced_service(
                        namespace=id, body=yaml_object)
                    print(("FL {} service created. Status={}").format(service_name, resp.metadata.name))
                except ApiException as e:
                    print(e.body)

            elif yaml_object['kind'] == 'Deployment':
                try:
                    for env in yaml_object['spec']['template']['spec']['containers'][0]['env']:
                        if env['name']=='PROBLEM_ID':
                            env['value'] = str(id)
                except KeyError as e:
                    print(e)

                try:
                    resp = apps_v1.create_namespaced_deployment(
                        namespace=id, body=yaml_object)
                    print(("FL {} deployment created. Status={}").format(service_name, resp.metadata.name))
                except ApiException as e:
                    print(e.body)

def create_pv(id, pv_config_file):
    core_v1 = client.CoreV1Api()
    # create a fl pv for each problem
    with open(pv_config_file) as f:
    # TODO: Add try catch
        dep = yaml.safe_load(f)
        try:
            dep['metadata']['name'] = str(id)
            dep['metadata']['labels']['fl-problem'] = str(id)
            resp = core_v1.create_persistent_volume(body=dep)
            print("FL PV created. status='%s'" % resp.metadata.name)
        except KeyError as e:
            print(e)
        except ApiException as e:
            # TODO: Handle AlreadyExists error
            print(e.body)

def create_namespaced_pvc(id, pvc_config_file):
    core_v1 = client.CoreV1Api()
    # create fl pvc under problem namespace
    with open(pvc_config_file) as f:
        dep = yaml.safe_load(f)
        try:
            dep['spec']['selector']['matchLabels']['fl-problem'] = str(id)
            resp = core_v1.create_namespaced_persistent_volume_claim(
                namespace=id, body=dep)
            print("FL PVC created. status='%s'" % resp.metadata.name)
        except KeyError as e:
            print(e.body)
        except ApiException as e:
            print(e.body)

def spawn_services(id):
    config.load_kube_config()
    core_v1 = client.CoreV1Api()

    # create the namespace as the fl problem id
    try:
        core_v1.read_namespace(str(id))
    except ApiException:
        create_namespace(str(id))

    # create a fl pv for each problem
    pv_config_file = os.path.join(
        settings.BASE_DIR, "k8s/fl-pv.yaml")
    create_pv(id, pv_config_file)

    # create fl coordinator service and deployment
    pvc_config_file = os.path.join(
        settings.BASE_DIR, "k8s/fl-pvc.yaml")
    create_namespaced_pvc(id, pvc_config_file)

    deployment_config_file = os.path.join(
        settings.BASE_DIR, "k8s/fl-coordinator.yaml")
    create_service_deployment(id, "Co-ordinator", deployment_config_file)

    # create fl selector service and deployment
    deployment_config_file = os.path.join(
        settings.BASE_DIR, "k8s/fl-selector.yaml")    
    create_service_deployment(id, "Selector", deployment_config_file)
