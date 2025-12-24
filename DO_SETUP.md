# Digital Ocean Kubernetes (DOKS) Setup Guide

This guide describes how to deploy the microservices and configure Ingress on your DOKS cluster.

## Prerequisites
- A Digital Ocean Kubernetes Cluster (DOKS).
- `kubectl` configured to communicate with your cluster.
- A domain name managed in Digital Ocean (or pointed to Digital Ocean's nameservers).

## 1. Install Nginx Ingress Controller

The easiest way to install the Nginx Ingress Controller on DOKS is using the official manifest:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/do/deploy.yaml
```

Wait for the ingress controller pod to be up and running and for the Load Balancer to be assigned an external IP.

```bash
kubectl get services -n ingress-nginx
```

Look for the `ingress-nginx-controller` service with `TYPE=LoadBalancer`. Note the `EXTERNAL-IP`.

## 2. Configure DNS

Go to your Digital Ocean Control Panel -> Networking -> Domains.
Add an `A` record for your domain (e.g., `example.com` or `app.example.com`) pointing to the `EXTERNAL-IP` you got in the previous step.

## 3. Deploy Microservices

Navigate to this directory and apply the manifests:

```bash
kubectl apply -f k8s/apps/
```

This will deploy the `frontend` and `backend` services.

## 4. Deploy Ingress

**IMPORTANT**: edit `k8s/ingress/ingress.yaml` and replace `example.com` with your actual domain name.

```bash
kubectl apply -f k8s/ingress/ingress.yaml
```

## 5. Verification

After a few minutes (DNS propagation), verify the endpoints:

- **Frontend**: `http://<YOUR_DOMAIN>/` -> Should see "Hello, world! Version: 1.0.0"
- **Backend**: `http://<YOUR_DOMAIN>/api` -> Should see "Hello, world! Version: 2.0.0"

## Directory Structure
- `k8s/apps/frontend.yaml`: Frontend deployment & service.
- `k8s/apps/backend.yaml`: Backend deployment & service.
- `k8s/ingress/ingress.yaml`: Ingress resource definition.
