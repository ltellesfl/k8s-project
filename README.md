# k8s-project

This project is a simple Kubernetes pod reader that reads the status of all pods in the cluster and writes the information to a table. The Docker image is deployed as a CronJob in a Kubernetes cluster using Helm.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Build](#build)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running outside the cluster](#running-outside-the-cluster)

## Prerequisites

- Kubernetes cluster (minikube, kind, etc.)
- Helm 3.x
- git
- Docker

## Build

To build the Docker image, use the following commands:

```sh
git clone https://github.com/ltellesfl/k8s-project.git
cd k8s-project
docker build -t k8s-project:latest .
```

If you are using kind, you can load the image into the cluster using the following command:

```sh
kind load docker-image k8s-project:latest
```

## Installation

To install the Helm chart, use the following commands:

```sh
git clone https://github.com/ltellesfl/k8s-project.git
cd k8s-project
helm install pod-reader ./chart
```

To upgrade the Helm chart, use the following commands:

```sh
helm upgrade pod-reader ./chart
```

## Configuration

The following table lists the configurable parameters of the Pod Reader chart and their default values.

| Parameter | Description | Default |
| --- | --- | --- |
| `name` | Cronjob and container name | `pod-reader` |
| `schedule` | Cronjob schedule | `*/5 * * * *` |
| `successfulJobsHistoryLimit` | Successful jobs history limit | `1` |
| `image` | Container image | `k8s-project:latest` |
| `imagePullPolicy` | Container image pull policy | `IfNotPresent` |
| `backoffLimit` | Number of retries before considering a job as failed | `1` |
| `podStatus` | The pod status to filter can be one of: `Terminating`, `Error`, `Completed`, `Running` or `CreateContainerConfigError` | `Running` |

## Running outside the cluster

To run the Pod Reader outside the cluster, you will need to have a running Kubernetes cluster and set the `POD_STATUS` environment variable to the desired pod status. The following commands show how to run the Pod Reader outside the cluster:
  
```sh
git clone https://github.com/ltellesfl/k8s-project.git
cd k8s-project
export POD_STATUS=Running
python3 app.py
```
