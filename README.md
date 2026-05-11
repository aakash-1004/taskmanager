# Task Manager — REST API with Kubernetes & Prometheus Observability

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat&logo=mongodb&logoColor=white)

A Flask REST API for task management deployed on Kubernetes with full observability via Prometheus and Grafana. Built as a DevOps golden thread project — demonstrating containerization, orchestration, and production monitoring.

---

## 📌 What It Does

A REST API that lets you:
- **Create** tasks with a title
- **Read** all tasks
- **Update** tasks (mark as done)
- **Delete** tasks
- **Health check** endpoint for Kubernetes probes

All data persisted in MongoDB. All HTTP metrics exported to Prometheus automatically.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check — returns `{"status": "ok"}` |
| `GET` | `/tasks` | Get all tasks |
| `POST` | `/tasks` | Create a new task |
| `PUT` | `/tasks/<id>` | Update a task |
| `DELETE` | `/tasks/<id>` | Delete a task |
| `GET` | `/metrics` | Prometheus metrics endpoint |

---

## 📝 Example Usage

```bash
# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Deploy to production"}'

# Get all tasks
curl http://localhost:5000/tasks

# Mark task as done
curl -X PUT http://localhost:5000/tasks/<id> \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete a task
curl -X DELETE http://localhost:5000/tasks/<id>
```

---

## 🏗️ Kubernetes Architecture

```
Kubernetes Cluster
├── Namespace: taskmanager
│   ├── Deployment (Flask API — 3 replicas)
│   ├── Service (ClusterIP)
│   ├── ConfigMap (app config)
│   ├── Secret (MongoDB URI)
│   └── HPA (auto-scales on CPU)
└── Namespace: monitoring
    ├── Prometheus (scrapes /metrics)
    └── Grafana (dashboards)
```

---

## 📊 Observability Stack

- **prometheus-flask-exporter** — automatically exports request count, latency, and status codes per endpoint
- **Prometheus** — scrapes `/metrics` endpoint, stores time-series data
- **Grafana** — visualizes request rate, error rate, and p95 latency via PromQL dashboards

Deployed via Helm:
```bash
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring
```

---

## 🚀 Running Locally

```bash
# Clone
git clone https://github.com/aakash-1004/taskmanager.git
cd taskmanager

# Run with Docker
docker build -t taskmanager:v1 .
docker run -d \
  -p 5000:5000 \
  -e MONGO_URI="mongodb://localhost:27017/" \
  -e DB_NAME="taskmanager" \
  taskmanager:v1
```

---

## ☸️ Deploy on Kubernetes

```bash
kubectl apply -f namespace.yaml
kubectl apply -f secret.yaml
kubectl apply -f configmap.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Database | MongoDB |
| Containerization | Docker |
| Orchestration | Kubernetes |
| Autoscaling | HPA |
| Metrics | prometheus-flask-exporter |
| Monitoring | Prometheus, Grafana |
| Deployment | Helm (kube-prometheus-stack) |
