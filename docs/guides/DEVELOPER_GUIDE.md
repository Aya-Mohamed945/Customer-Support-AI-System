# 👨‍💻 Developer Guide — Customer Support AI

> Complete technical guide for developers setting up, customizing, testing, and deploying the Customer Support AI system.

---

## 📋 Table of Contents

* [Overview](#overview)
* [System Architecture](#system-architecture)

  * [High-Level Architecture](#high-level-architecture)
  * [Technology Stack](#technology-stack)
* [Development Setup](#development-setup)

  * [Prerequisites](#prerequisites)
  * [Local Installation](#local-installation)
  * [Environment Configuration](#environment-configuration)
  * [Docker Installation](#docker-installation)
* [Project Structure](#project-structure)
* [Machine Learning](#machine-learning)

  * [Training Pipeline](#training-pipeline)
  * [Training Commands](#training-commands)
  * [Model Configuration](#model-configuration)
* [API Development](#api-development)

  * [Adding a New Endpoint](#adding-a-new-endpoint)
  * [Modifying ML Models](#modifying-ml-models)
  * [Adding New Features](#adding-new-features)
* [RAG Development](#rag-development)

  * [Adding FAQs](#adding-faqs)
  * [Rebuilding the FAQ Index](#rebuilding-the-faq-index)
  * [Customizing Embeddings](#customizing-embeddings)
* [Frontend Development](#frontend-development)

  * [Component Structure](#component-structure)
  * [Adding Pages](#adding-pages)
  * [API Integration](#api-integration)
* [Testing](#testing)

  * [Backend Testing](#backend-testing)
  * [Frontend Testing](#frontend-testing)
* [Deployment](#deployment)

  * [Environment Variables](#environment-variables)
  * [Deployment Commands](#deployment-commands)
* [CI/CD Pipeline](#cicd-pipeline)
* [Troubleshooting](#troubleshooting)
* [Contributing Guidelines](#contributing-guidelines)
* [Additional Resources](#additional-resources)
* [Support](#support)

---

## 🎯 Overview

Customer Support AI is an AI-powered customer support system designed to automatically analyze customer support tickets and provide intelligent assistance.

The system combines machine learning, natural language processing, and Retrieval-Augmented Generation (RAG) to provide:

* **Category Classification** — Identifies the type of customer issue.
* **Priority Prediction** — Determines the urgency of the ticket.
* **Sentiment Analysis** — Identifies the customer's emotional state.
* **Smart Solutions** — Retrieves relevant answers from the FAQ knowledge base.
* **Ticket History** — Allows users to review previously submitted tickets.
* **Monitoring & Analytics** — Provides system-level performance metrics.

### Core Technologies

| Component               | Technology                  |
| ----------------------- | --------------------------- |
| Backend API             | FastAPI                     |
| Programming Language    | Python 3.11                 |
| Machine Learning        | scikit-learn                |
| NLP                     | NLTK, Sentence Transformers |
| Vector Search           | FAISS                       |
| Frontend                | Next.js 14                  |
| Frontend Language       | TypeScript                  |
| Styling                 | Tailwind CSS                |
| Containerization        | Docker                      |
| Container Orchestration | Docker Compose              |

This guide is intended for developers who need to:

* Set up the project locally.
* Understand the system architecture.
* Train or modify ML models.
* Extend the API.
* Customize the RAG pipeline.
* Develop new frontend features.
* Run tests.
* Deploy the application.
* Troubleshoot common issues.

---

# 🏗️ System Architecture

## High-Level Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                   │
│                                                                             │
│   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────────┐   │
│   │     Web App      │   │   Mobile App     │   │      API Client      │   │
│   │    Next.js       │   │     Future       │   │       cURL           │   │
│   └────────┬─────────┘   └────────┬─────────┘   └──────────┬───────────┘   │
│            │                      │                        │               │
│            └──────────────────────┼────────────────────────┘               │
│                                   ▼                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                         API / APPLICATION LAYER                             │
│                                                                             │
│                         ┌──────────────────────┐                            │
│                         │       FastAPI        │                            │
│                         │      Port 8000       │                            │
│                         └──────────┬───────────┘                            │
│                                    │                                        │
│          ┌─────────────────────────┼──────────────────────────┐             │
│          │                         │                          │             │
│          ▼                         ▼                          ▼             │
│   ┌──────────────┐        ┌───────────────┐        ┌─────────────────┐     │
│   │ Predictions  │        │ Authentication │        │    Metrics      │     │
│   │  /predict    │        │   /auth/*      │        │    /metrics     │     │
│   └──────┬───────┘        └───────────────┘        └─────────────────┘     │
│          │                                                                  │
│          ▼                                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                         SERVICE LAYER                               │   │
│   │                                                                     │   │
│   │  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────────┐ │   │
│   │  │   ML Pipeline    │  │    RAG Service   │  │    Monitoring     │ │   │
│   │  │                  │  │                  │  │      Service      │ │   │
│   │  │ • Category       │  │ • Embeddings     │  │ • Metrics         │ │   │
│   │  │ • Priority       │  │ • FAISS Index    │  │ • Error Logs      │ │   │
│   │  │ • Sentiment      │  │ • FAQ Metadata   │  │ • Performance     │ │   │
│   │  └──────────────────┘  └──────────────────┘  └───────────────────┘ │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
├────────────────────────────────────┼────────────────────────────────────────┤
│                              DATA LAYER                                     │
│                                    │                                        │
│       ┌────────────────┐  ┌────────┴────────┐  ┌──────────────────────┐    │
│       │ Trained Models │  │   Data Files     │  │    Application Logs  │    │
│       │     .pkl       │  │      .csv        │  │       .log           │    │
│       └────────────────┘  └─────────────────┘  └──────────────────────┘    │
│                                                                             │
│                            users.json                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Main Services

| Service     | Purpose                           | Default Port |
| ----------- | --------------------------------- | -----------: |
| Frontend    | User interface                    |       `3000` |
| Backend API | REST API and ML predictions       |       `8000` |
| RAG Service | FAQ retrieval and semantic search |       `8001` |

---

## Technology Stack

| Layer            | Technology            | Version   |
| ---------------- | --------------------- | --------- |
| API              | FastAPI               | `0.115.6` |
| ML               | scikit-learn          | `1.6.1`   |
| NLP              | NLTK                  | `3.9.1`   |
| Embeddings       | Sentence Transformers | `3.3.1`   |
| Vector Database  | FAISS                 | `1.9.0`   |
| Frontend         | Next.js               | `14.2.5`  |
| Language         | TypeScript            | `5.x`     |
| Styling          | Tailwind CSS          | `3.4.1`   |
| Python           | Python                | `3.11`    |
| Containerization | Docker                | Latest    |
| Orchestration    | Docker Compose        | Latest    |

---

# 🔧 Development Setup

## Prerequisites

Make sure the following tools are installed before starting development.

| Tool    | Recommended Version | Check              |
| ------- | ------------------- | ------------------ |
| Python  | `3.11+`             | `python --version` |
| Node.js | `20.x+`             | `node --version`   |
| npm     | `10.x+`             | `npm --version`    |
| Docker  | `24.x+`             | `docker --version` |
| Git     | `2.x+`              | `git --version`    |

---

## Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Aya-Mohamed945/customer-support-ai.git
cd customer-support-ai
```

---

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows

```powershell
.venv\Scripts\activate
```

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Install production dependencies:

```bash
pip install -r requirements.txt
```

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Create required directories if they do not already exist:

```bash
mkdir models
mkdir data
mkdir logs
```

Copy the environment template:

#### Linux / macOS

```bash
cp .env.example .env
```

#### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Edit `.env` using your preferred editor.

---

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Copy the environment template:

#### Linux / macOS

```bash
cp .env.local.example .env.local
```

#### Windows PowerShell

```powershell
Copy-Item .env.local.example .env.local
```

Edit `.env.local` using your preferred editor.

---

## Environment Configuration

### Backend `.env`

Example development configuration:

```env
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=True
LOG_LEVEL=DEBUG

SECRET_KEY=your-dev-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

RAG_URL=http://localhost:8001

HF_HUB_ENABLE_HF_TRANSFER=0
HF_HUB_DOWNLOAD_TIMEOUT=300

MODELS_DIR=./models
DATA_DIR=./data

BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

> **Security:** Never commit a real `SECRET_KEY` or other sensitive credentials to Git.

### Frontend `.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Customer Support AI
```

---

## Docker Installation

Build all services:

```bash
docker-compose build
```

Start the services:

```bash
docker-compose up -d
```

View service logs:

```bash
docker-compose logs -f
```

Stop the services:

```bash
docker-compose down
```

Rebuild without using the Docker cache:

```bash
docker-compose build --no-cache
docker-compose up -d
```

---

# 📁 Project Structure

```text
customer-support-ai/
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── cd.yml
│   │   └── security.yml
│   └── dependabot.yml
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── auth.py
│   │   │   └── models.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├── pipeline.py
│   │   │   ├── preprocessing.py
│   │   │   └── feature_extraction.py
│   │   │
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── service.py
│   │   │   └── api.py
│   │   │
│   │   ├── monitoring/
│   │   │   ├── __init__.py
│   │   │   └── metrics.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── logger.py
│   │
│   ├── models/
│   ├── data/
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   └── Dockerfile.rag
│   ├── scripts/
│   │   ├── train_models.py
│   │   └── build_faq_v2.py
│   ├── tests/
│   ├── run.py
│   ├── run_rag.py
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── Makefile
│   └── .env.example
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   ├── signup/
│   │   ├── dashboard/
│   │   ├── history/
│   │   ├── components/
│   │   ├── utils/
│   │   └── types/
│   │
│   ├── public/
│   ├── tests/
│   ├── Dockerfile.frontend
│   ├── package.json
│   ├── next.config.mjs
│   ├── tailwind.config.ts
│   └── tsconfig.json
│
├── docker/
│   └── docker-compose.yml
│
├── docs/
│   ├── architecture/
│   ├── backend/
│   └── guides/
│       ├── DEVELOPER_GUIDE.md
│       └── USER_GUIDE.md
│
├── scripts/
│   └── deploy.sh
│
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── Makefile
└── README.md
```

---

# 🧠 Machine Learning

## Training Pipeline

The system uses separate models for ticket classification tasks.

### Priority Model

```python
def train_priority_model():
    """
    Train the ticket priority classification model.

    Model:
        Logistic Regression

    Configuration:
        20 clusters / groups
        5-Fold Cross-Validation
    """
    # Load data
    # Preprocess text
    # Extract features
    # Train model
    # Evaluate model
    # Save trained model
```

### Category Model

```python
def train_category_model():
    """
    Train the ticket category classification model.

    Classes:
        account
        billing
        delivery
        technical
    """
    # Load data
    # Preprocess text
    # Extract features
    # Train model
    # Evaluate model
    # Save trained model
```

### Sentiment Model

```python
def train_sentiment_model():
    """
    Train the ticket sentiment classification model.

    Classes:
        positive
        neutral
        negative
        angry
    """
    # Load data
    # Preprocess text
    # Extract features
    # Train model
    # Evaluate model
    # Save trained model
```

---

## Training Commands

Train all models:

```bash
python scripts/train_models.py
```

Train the priority model only:

```bash
python -c "from scripts.train_models import train_priority_model; train_priority_model()"
```

Build or rebuild the FAQ database:

```bash
python scripts/build_faq_v2.py
```

---

## Model Configuration

| Model     | Parameter      |    Value |
| --------- | -------------- | -------: |
| Priority  | `max_features` |   `3000` |
| Priority  | `ngram_range`  | `(1, 2)` |
| Priority  | `C`            |    `0.5` |
| Priority  | Clusters       |     `20` |
| Category  | `max_features` |  `10000` |
| Category  | `C`            |    `1.0` |
| Sentiment | `max_features` |   `5000` |
| Sentiment | `C`            |   `10.0` |

---

# 🔌 API Development

## Adding a New Endpoint

### Step 1 — Create Request/Response Models

Add the required Pydantic models to:

```text
backend/app/api/models.py
```

Example:

```python
from typing import Optional

from pydantic import BaseModel, Field


class NewRequest(BaseModel):
    field1: str = Field(..., min_length=1)
    field2: Optional[int] = None


class NewResponse(BaseModel):
    result: str
    confidence: float
```

---

### Step 2 — Add the Endpoint

Add the endpoint to:

```text
backend/app/api/routes.py
```

Example:

```python
from fastapi import HTTPException


@router.post("/new-endpoint", response_model=NewResponse)
async def new_endpoint(request: NewRequest):
    """
    Process a new request and return the result.
    """
    try:
        result = some_function(request.field1)

        return NewResponse(
            result=result,
            confidence=0.95,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
```

---

### Step 3 — Register the Router

If a separate router is created, register it in:

```text
backend/app/main.py
```

Example:

```python
from app.api.routes import router as main_router
from app.api.new_routes import router as new_router

app.include_router(
    main_router,
    prefix="/api/v1",
)

app.include_router(
    new_router,
    prefix="/api/v1",
)
```

---

## Modifying ML Models

### 1. Update Preprocessing

File:

```text
backend/app/ml/preprocessing.py
```

Example:

```python
def preprocess_text(text: str) -> str:
    """
    Apply the required text preprocessing steps.
    """
    text = custom_function(text)

    return text
```

When modifying preprocessing, ensure that the same preprocessing logic is applied during both training and inference.

---

### 2. Update Feature Extraction

File:

```text
backend/app/ml/feature_extraction.py
```

Example:

```python
import numpy as np


def extract_advanced_features(text: str) -> np.ndarray:
    """
    Extract additional features from the input text.
    """
    new_feature = calculate_new_feature(text)

    return np.array([[new_feature]])
```

---

### 3. Update the Prediction Pipeline

File:

```text
backend/app/ml/pipeline.py
```

Example:

```python
class PredictionPipeline:

    def predict(self, title, description, resolution_time):
        """
        Generate predictions using the trained models.
        """
        # Build features
        # Generate predictions
        # Calculate confidence
        # Return results

        new_prediction = self.new_model.predict(features)

        return updated_results
```

> After changing the preprocessing, feature extraction, or model architecture, retrain and validate the affected model before deploying it.

---

# 🔍 RAG Development

The RAG component retrieves relevant FAQ entries based on the semantic similarity between the submitted ticket and the knowledge base.

## Adding FAQs

FAQs are stored in:

```text
backend/data/faq_combined.csv
```

The expected structure is:

```text
question,answer,category,domain
```

Example:

```csv
question,answer,category,domain
"I was charged twice","Please contact support with your order number.","billing","payments"
```

When adding new FAQs:

1. Add the question and answer.
2. Assign the appropriate category.
3. Assign the appropriate domain.
4. Validate the CSV format.
5. Rebuild the vector index.

---

## Rebuilding the FAQ Index

After modifying the FAQ dataset, rebuild the index:

```bash
python scripts/build_faq_v2.py
```

This ensures that the new FAQ entries are included in semantic retrieval.

---

## Customizing Embeddings

The RAG service is located at:

```text
backend/app/rag/service.py
```

Example:

```python
from sentence_transformers import SentenceTransformer


class RAGService:

    def __init__(self):
        self.model = SentenceTransformer(
            "your-model-name"
        )
```

When changing the embedding model:

* Verify that the model is compatible with the existing pipeline.
* Rebuild the FAISS index.
* Evaluate retrieval quality.
* Verify that API responses remain compatible with the frontend.

---

# ⚛️ Frontend Development

## Component Structure

The frontend follows a component-based Next.js architecture.

```text
frontend/app/
│
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Toast.tsx
│   │   └── LoadingSkeleton.tsx
│   │
│   ├── dashboard/
│   │   ├── MetricsCard.tsx
│   │   ├── Chart.tsx
│   │   └── RecentActivity.tsx
│   │
│   ├── TicketForm.tsx
│   └── ResultsDisplay.tsx
│
├── utils/
│   └── api.ts
│
└── types/
    └── index.ts
```

---

## Adding a New Page

Create a new page under:

```text
frontend/app/new-page/page.tsx
```

Example:

```tsx
'use client';

import { useEffect, useState } from 'react';

export default function NewPage() {
    const [data, setData] = useState(null);

    useEffect(() => {
        // Fetch required data.
        fetchData();
    }, []);

    return (
        <div className="min-h-screen">
            {/* Page content */}
        </div>
    );
}
```

Follow the existing project conventions for:

* Component naming.
* TypeScript types.
* API calls.
* Error handling.
* Loading states.
* Responsive design.
* Tailwind CSS classes.

---

## API Integration

The API client is located at:

```text
frontend/app/utils/api.ts
```

Example:

```typescript
export async function newEndpoint(
    data: NewRequest
): Promise<NewResponse> {

    const response = await fetch(
        `${API_BASE_URL}/api/v1/new-endpoint`,
        {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        }
    );

    if (!response.ok) {
        throw new Error('Failed to call endpoint');
    }

    return response.json();
}
```

When adding a new API endpoint:

1. Define the request type.
2. Define the response type.
3. Add the API function.
4. Handle loading and error states.
5. Integrate the function into the required component or page.

---

# 🧪 Testing

## Backend Testing

Run all backend tests:

```bash
pytest tests/ -v
```

Run tests with coverage:

```bash
pytest tests/ --cov=app --cov-report=html
```

Run a specific test:

```bash
pytest tests/test_api.py::TestPrediction::test_predict_success -v
```

Run tests in parallel:

```bash
pytest tests/ -n auto
```

---

## Frontend Testing

Run all tests:

```bash
npm run test
```

Run tests with coverage:

```bash
npm run test:coverage
```

Run tests in watch mode:

```bash
npm run test:watch
```

Run a specific test:

```bash
npm test -- TicketForm.test.tsx
```

---

# 🚀 Deployment

## Environment Variables

The following environment variables are required or recommended for deployment.

| Variable               | Description              | Required |
| ---------------------- | ------------------------ | :------: |
| `SECRET_KEY`           | JWT secret key           |     ✅    |
| `RAG_URL`              | RAG service URL          |     ✅    |
| `BACKEND_CORS_ORIGINS` | Allowed frontend origins |     ✅    |
| `API_HOST`             | API host binding         |     ❌    |
| `API_PORT`             | API port                 |     ❌    |
| `DEBUG`                | Debug mode               |     ❌    |
| `LOG_LEVEL`            | Application log level    |     ❌    |

> **Production:** Use secure, environment-specific values and never commit secrets to source control.

---

## Deployment Commands

### Local Development

Run the backend and RAG services:

```bash
python run.py
python run_rag.py
```

### Docker Development

```bash
docker-compose up -d
```

### Production Docker

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes

Kubernetes deployment is planned for future versions.

Example:

```bash
kubectl apply -f k8s/
```

---

# 🔄 CI/CD Pipeline

The project uses GitHub Actions workflows for automated testing, deployment, and security checks.

## 1. CI Pipeline

File:

```text
.github/workflows/ci.yml
```

The CI pipeline is responsible for:

* Running backend tests.
* Running frontend tests.
* Collecting test coverage.
* Validating ML components.
* Building Docker images.

---

## 2. CD Pipeline

File:

```text
.github/workflows/cd.yml
```

The deployment pipeline can be configured to:

* Build Docker images.
* Push images to a container registry.
* Deploy to staging.
* Deploy to production.
* Run post-deployment health checks.

---

## 3. Security Scanning

File:

```text
.github/workflows/security.yml
```

Security checks may include:

* Dependency vulnerability scanning.
* Static Application Security Testing (SAST).
* Bandit security analysis.
* Trivy container scanning.

---

## Required CI/CD Secrets

| Secret                  | Description           |
| ----------------------- | --------------------- |
| `DOCKER_USERNAME`       | Docker Hub username   |
| `DOCKER_PASSWORD`       | Docker Hub password   |
| `AWS_ACCESS_KEY_ID`     | AWS access key        |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key |
| `STAGING_HOST`          | Staging server        |
| `PRODUCTION_HOST`       | Production server     |

Only configure the secrets required by the deployment environment.

---

# 🔧 Troubleshooting

## 1. `ModuleNotFoundError`

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Verify the Python environment:

```bash
python --version
```

If necessary, activate the virtual environment again.

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Check the Python path:

```bash
python -c "import sys; print(sys.path)"
```

---

## 2. CUDA / GPU Issues

If GPU-specific FAISS causes compatibility issues, use the CPU version:

```bash
pip uninstall faiss-gpu
pip install faiss-cpu
```

Check CUDA availability:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

## 3. Memory Issues

Set Python to use unbuffered output:

```bash
export PYTHONUNBUFFERED=1
```

Limit OpenMP threads when necessary:

```bash
export OMP_NUM_THREADS=4
```

For Windows PowerShell:

```powershell
$env:PYTHONUNBUFFERED="1"
$env:OMP_NUM_THREADS="4"
```

For training workloads, consider:

* Reducing batch sizes.
* Reducing the number of features.
* Processing data in smaller chunks.
* Using CPU-friendly configurations.

---

## 4. Docker Build Fails

Clear unused Docker resources:

```bash
docker system prune -a
```

Rebuild without cache:

```bash
docker-compose build --no-cache
```

Inspect service logs:

```bash
docker-compose logs -f
```

Check the status of running containers:

```bash
docker-compose ps
```

---

# 🤝 Contributing Guidelines

## Code Style

Run Black:

```bash
black app/ scripts/ tests/
```

Run isort:

```bash
isort app/ scripts/ tests/
```

Run flake8:

```bash
flake8 app/ --max-line-length=120
```

Run mypy:

```bash
mypy app/
```

---

## Commit Convention

Use clear and consistent commit messages.

```text
feat: Add new feature
fix: Fix prediction API error
docs: Update developer guide
style: Format frontend components
refactor: Refactor prediction pipeline
test: Add API tests
chore: Update dependencies
```

Recommended format:

```text
<type>: <short description>
```

---

## Pull Request Process

Before opening a pull request:

1. Create a feature branch.
2. Implement the required changes.
3. Add or update tests.
4. Run the test suite.
5. Run formatting and linting tools.
6. Update the documentation when necessary.
7. Review the changes locally.
8. Submit the pull request.

Recommended branch naming:

```text
feature/<feature-name>
fix/<bug-name>
docs/<documentation-name>
refactor/<component-name>
```

---

# 📚 Additional Resources

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [scikit-learn Documentation](https://scikit-learn.org/)
* [Next.js Documentation](https://nextjs.org/docs)
* [Docker Documentation](https://docs.docker.com/)
* [Sentence Transformers Documentation](https://www.sbert.net/)
* [FAISS Documentation](https://faiss.ai/)

---

# 📞 Support

For project-related issues:

* **GitHub Issues:** https://github.com/Aya-Mohamed945/Customer-Support-AI-System/issues

* **Project Repository:** https://github.com/Aya-Mohamed945/Customer-Support-AI-System

For internal project support, use the project's designated communication channel.

---

<div align="center">

<strong>Customer Support AI — Developer Guide</strong>

<br>

Last Updated: August 2026

</div>
