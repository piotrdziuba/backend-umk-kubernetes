# Declarative approach

## Create a deployment and a service

### 1. Initial deployment
```bash
kubectl apply -f 01_load-balancer-initial.yaml
```
Check pods:
```bash
kubectl get pods
````

### 2. Scale the deployment
```bash
kubectl apply -f 02_load-balancer-scaled.yaml
```

#### Check pods:
```bash
kubectl get pods
```

### 3. Expose the deployment as a service
```bash
kubectl apply -f 03_load-balancer-service.yaml
```

#### Check services:
```bash
kubectl get services
```

#### Provide a routable interface to the my-service:
```bash
minikube service my-service --url
```

Open the URL in the browser or use curl to see the response from the service. Refresh page several times
and observe the response host.

##  Cleanup
```bash
kubectl delete service my-service
kubectl delete deployment hello-world
```