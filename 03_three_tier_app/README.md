# Three-Tier Chat App — Minikube

A simple chat application built with three tiers:

| Tier | Technology | File |
|------|------------|------|
| Frontend | nginx (reverse proxy) | `frontend/frontend.yaml` |
| Application | Python / Flask | `backend/app.py` + `backend/Dockerfile` |
| Data | Redis | `backend/backend.yaml` |

```
three-tier-app/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── backend.yaml      # Redis Deployment + PVC + Secret
└── frontend/
    └── frontend.yaml     # nginx ConfigMap + Deployment
```

---

## Requirements

- [minikube](https://minikube.sigs.k8s.io/docs/start/) ≥ 1.32
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Docker](https://docs.docker.com/get-docker/) or Podman

---

## 1. Start minikube

```bash
minikube start --driver=podman --container-runtime=cri-o
```

---

## 2. Build the Flask image and load it into minikube

minikube uses its own container runtime, so we need to build the Flask app image and load it into minikube's runtime. 
If you're using Docker, you can use `minikube image load` directly. 
With Podman, we can save the image and pipe it into `minikube image load`.

```bash
podman build -t flask-app:latest ./backend
podman save flask-app:latest | minikube image load --overwrite=true -

# Verify:
minikube image ls | grep flask-app
```

---

## 3. Deploy the data layer (Redis) and Flask app

```bash
kubectl apply -f backend/backend.yaml
```

Check that all services are up:

```bash
kubectl rollout status deployment/backend-redis
kubectl rollout status deployment/flask-app
```

---

## 4. Deploy the frontend (nginx proxy)

```bash
kubectl apply -f frontend/frontend.yaml
```

---

## 5. Open the app in the browser

```bash
minikube service frontend
```

minikube will automatically open the URL in the browser.

Alternatively, use port-forward:

```bash
kubectl port-forward svc/frontend 8080:80
# Open http://localhost:8080
```

---

## Checking status

```bash
# All pods
kubectl get pods

# Flask logs
kubectl logs deployment/flask-app

# nginx logs
kubectl logs deployment/frontend

# API healthcheck
curl $(minikube service frontend --url)/health
```

---

## Stopping and cleanup

```bash
# Remove all resources
kubectl delete -f frontend/frontend.yaml
kubectl delete -f backend/backend.yaml

# Or stop the entire cluster
minikube stop
```

