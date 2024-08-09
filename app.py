import logging
import os
import sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from tabulate import tabulate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Check if POD_STATUS environment variable is set
pod_status = os.getenv("POD_STATUS")
if not pod_status:
    logging.error("POD_STATUS environment variable is not set")
    sys.exit(1)

try:
    # Load Kubernetes configuration
    if os.getenv('KUBERNETES_SERVICE_HOST'):
        config.load_incluster_config()
    else:
        config.load_kube_config()
        logging.info("Running using local kube config file")
    
    # Initialize Kubernetes client
    v1 = client.CoreV1Api()
    logging.info("Kubernetes client initialized")
    logging.info("Listing pods with %s status", pod_status)
    pods = v1.list_pod_for_all_namespaces(watch=False)

except ApiException as e:
    logging.error("Error interacting with Kubernetes API: %s", e)
    sys.exit(1)
except Exception as e:
    logging.error("Unexpected error: %s", e)
    sys.exit(1)

# Initialize the table with headers
table = [["Namespace", "Name", "PodIP", "Status"]]

# Iterate through the pods and filter based on the status
for pod in pods.items:
    # Check for Terminating status
    if pod_status == "Terminating" and pod.metadata.deletion_timestamp:
        table.append([pod.metadata.namespace, pod.metadata.name, pod.status.pod_ip, pod_status])
        continue

    # Check container statuses
    for status in pod.status.container_statuses:
        if pod.status.phase == pod_status and status.state.running and not pod.metadata.deletion_timestamp:
            table.append([pod.metadata.namespace, pod.metadata.name, pod.status.pod_ip, pod_status])
        elif status.state.terminated and status.state.terminated.reason == pod_status:
            table.append([pod.metadata.namespace, pod.metadata.name, pod.status.pod_ip, status.state.terminated.reason])
        elif status.state.waiting and status.state.waiting.reason == pod_status:
            table.append([pod.metadata.namespace, pod.metadata.name, pod.status.pod_ip, status.state.waiting.reason])
        elif status.last_state.terminated and status.last_state.terminated.reason == pod_status:
            table.append([pod.metadata.namespace, pod.metadata.name, pod.status.pod_ip, status.last_state.terminated.reason])

if len(table) == 1:
    logging.info("No pods with %s status found", pod_status)
else:
    logging.info("\n%s", tabulate(table, headers="firstrow", tablefmt="rst"))
