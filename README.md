# Interactive DevOps Application

A simple interactive web application built with FastAPI and vanilla HTML/JavaScript, designed for deployment with Kubernetes and Argo CD.

## Features

- **FastAPI Backend**: Modern Python web framework with automatic API documentation
- **Interactive Frontend**: Clean, responsive HTML/JavaScript interface
- **Health Monitoring**: Built-in health check endpoint for Kubernetes probes
- **Message Processing**: RESTful API for message submission and processing
- **Container Ready**: Optimized Docker image with security best practices
- **Kubernetes Native**: Complete Helm chart with ingress, service, and deployment
- **GitOps Ready**: Argo CD application configuration for automated deployment

## API Endpoints

- `GET /healthz` - Health check endpoint
- `POST /api/submit` - Submit a message (accepts JSON: `{"message": "your text"}`)
- `GET /api/info` - Application information and available endpoints
- `GET /` - Web interface (static HTML)

## Local Development

### Prerequisites

- Python 3.11+
- Docker (optional)

### Running with Python

1. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Start the application:
```bash
python backend/app.py
```

3. Open your browser to `http://localhost:8000`

### Running with Docker

1. Build the image:
```bash
docker build -t interactiveapp:latest .
```

2. Run the container:
```bash
docker run -p 8000:8000 interactiveapp:latest
```

3. Access the application at `http://localhost:8000`

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster with Helm 3.x
- Argo CD installed and configured
- Ingress controller (nginx recommended)

### Deploy with Argo CD

1. **Apply the Argo CD Application**:
```bash
kubectl apply -f k8s/interactiveapp-argocd.yaml
```

2. **Sync the Application**:
```bash
# Using Argo CD CLI
argocd app sync interactiveapp --insecure

# Or sync via the web UI at your Argo CD dashboard
```

3. **Verify Deployment**:
```bash
kubectl get pods -n skillflight
kubectl get svc -n skillflight
kubectl get ingress -n skillflight
```

### Manual Helm Deployment

If you prefer to deploy directly with Helm:

```bash
# Install the application
helm install interactiveapp ./helm/interactiveapp -n skillflight --create-namespace

# Upgrade the application
helm upgrade interactiveapp ./helm/interactiveapp -n skillflight

# Uninstall the application
helm uninstall interactiveapp -n skillflight
```

## Accessing the Application

### Local Development
- Application: `http://localhost:8000`
- Health Check: `http://localhost:8000/healthz`
- API Docs: `http://localhost:8000/docs`

### Kubernetes Deployment
- Application: `http://interactiveapp.local` (add to `/etc/hosts` if needed)
- NodePort Access: `http://<NODE_IP>:30080` (direct access via any cluster node)
- Health Check: `http://interactiveapp.local/healthz`

To access via `interactiveapp.local`, add this line to your `/etc/hosts`:
```
<INGRESS_IP> interactiveapp.local
```

Get your ingress IP with:
```bash
kubectl get ingress -n skillflight
```

## Configuration

### Helm Values

Key configuration options in `helm/interactiveapp/values.yaml`:

- `replicaCount`: Number of pod replicas (default: 1)
- `image.repository`: Docker image repository
- `image.tag`: Docker image tag
- `service.port`: Service port (default: 80)
- `ingress.hosts`: Ingress hostnames
- `resources`: CPU and memory limits/requests
- `env`: Environment variables

### Environment Variables

- `ENVIRONMENT`: Deployment environment (development/production)

## Monitoring & Health Checks

The application includes comprehensive health monitoring:

- **Liveness Probe**: `GET /healthz` - Ensures the application is running
- **Readiness Probe**: `GET /healthz` - Ensures the application is ready to serve traffic
- **Docker Health Check**: Built-in container health verification

## Security Features

- Non-root user execution in containers
- Security contexts with dropped capabilities
- Read-only root filesystem options
- Resource limits and requests
- Service account with minimal permissions

## Development & Contributing

### Project Structure
```
devops-test/
├── backend/           # FastAPI application
│   ├── app.py        # Main application file
│   └── requirements.txt
├── frontend/          # Static web files
│   └── index.html    # Main web interface
├── helm/             # Kubernetes Helm chart
│   └── interactiveapp/
├── k8s/              # Kubernetes manifests
├── Dockerfile        # Container image definition
└── README.md         # This file
```

### Making Changes

1. **Backend Changes**: Modify `backend/app.py` for API changes
2. **Frontend Changes**: Update `frontend/index.html` for UI changes
3. **Deployment Changes**: Update Helm templates in `helm/interactiveapp/templates/`
4. **Configuration Changes**: Modify `helm/interactiveapp/values.yaml`

### Testing

Test the health endpoint:
```bash
curl http://localhost:8000/healthz
```

Test the API endpoint:
```bash
curl -X POST http://localhost:8000/api/submit \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from DevOps!"}'
```

## Troubleshooting

### Common Issues

1. **Pod not starting**: Check logs with `kubectl logs -n skillflight <pod-name>`
2. **Ingress not working**: Verify ingress controller and DNS/hosts configuration
3. **Health check failing**: Ensure the `/healthz` endpoint is accessible

### Debug Commands

```bash
# Check pod status
kubectl get pods -n skillflight -l app.kubernetes.io/name=interactiveapp

# View pod logs
kubectl logs -n skillflight -l app.kubernetes.io/name=interactiveapp

# Check service endpoints
kubectl get endpoints -n skillflight

# Verify ingress configuration
kubectl describe ingress -n skillflight
```

## License

This project is part of a DevOps demonstration and is available for educational and testing purposes.