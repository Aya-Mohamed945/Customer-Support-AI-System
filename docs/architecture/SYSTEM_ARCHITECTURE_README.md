Customer Support AI — System Architecture
> End-to-end architecture documentation for the **Customer Support AI** platform.
---
Table of Contents
Overview
Key Capabilities
High-Level Architecture
Component Architecture
API Gateway
ML Pipeline
RAG Service
Monitoring Service
Authentication Service
End-to-End Data Flow
Technology Stack
Security Architecture
Monitoring & Observability
Scalability
Deployment Architecture
Future Enhancements
Related Documentation
Architecture Ownership
---
Overview
Customer Support AI is a microservices-based system designed to automate customer support ticket analysis and assist support teams with intelligent ticket understanding and solution retrieval.
The platform combines:
Machine Learning for ticket classification across Category, Priority, and Sentiment
Retrieval-Augmented Generation (RAG) for intelligent FAQ and solution retrieval
FastAPI for high-performance API delivery
Next.js for the web application
Docker and Docker Compose for containerization and deployment
JWT-based authentication with role-based access control
Monitoring and observability for prediction and system metrics
Key Capabilities
Capability	Description
Ticket Classification	Automatically categorizes tickets into 4 categories
Priority Prediction	Predicts ticket priority (High / Medium / Low) with 98.84% accuracy
Sentiment Analysis	Detects customer sentiment across 4 classes with 89.58% accuracy
Intelligent Retrieval	Uses semantic search to retrieve relevant FAQ solutions
User Management	JWT-based authentication with role-based access control
Prediction Monitoring	Tracks predictions, errors, confidence scores, and response times
---
High-Level Architecture
```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│                                                                              │
│   ┌────────────────┐     ┌────────────────┐     ┌────────────────────┐      │
│   │    Web App     │     │  Mobile App    │     │    API Client      │      │
│   │    Next.js     │     │    Future      │     │    cURL / HTTP     │      │
│   └───────┬────────┘     └───────┬────────┘     └──────────┬─────────┘      │
│           │                      │                         │                │
│           └──────────────────────┼─────────────────────────┘                │
│                                  ▼                                          │
│   ┌──────────────────────────────────────────────────────────────────────┐ │
│   │                         API GATEWAY — Port 8000                        │ │
│   │                              FastAPI                                  │ │
│   │                                                                      │ │
│   │   /predict       /auth/*       /metrics       /rag/retrieve          │ │
│   └────────────┬──────────────┬──────────────┬──────────────┬─────────────┘ │
│                │              │              │              │               │
│                ▼              ▼              ▼              ▼               │
│   ┌──────────────────────────────────────────────────────────────────────┐ │
│   │                           SERVICE LAYER                               │ │
│   │                                                                      │ │
│   │  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────┐ │ │
│   │  │    ML Pipeline    │  │    RAG Service      │  │   Monitoring   │ │ │
│   │  │                    │  │    Port 8001        │  │    Service     │ │ │
│   │  │ • Category         │  │ • Sentence         │  │ • Metrics      │ │ │
│   │  │ • Priority         │  │   Transformer      │  │   Collector    │ │ │
│   │  │ • Sentiment        │  │ • FAISS Index      │  │ • Error Logs   │ │ │
│   │  └────────────────────┘  │ • FAQ Metadata     │  └────────────────┘ │ │
│   │                          └────────────────────┘                       │ │
│   └──────────────────────────────────────────────────────────────────────┘ │
│                                  │                                          │
│                                  ▼                                          │
│   ┌──────────────────────────────────────────────────────────────────────┐ │
│   │                             DATA LAYER                                │ │
│   │                                                                      │ │
│   │   Models (.pkl)   │   Data (.csv)   │   Logs (.log)   │ users.json   │ │
│   └──────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```
---
Component Architecture
1. API Gateway
The FastAPI API Gateway is the primary entry point for client requests. It validates incoming requests, handles authentication, exposes system endpoints, and coordinates the prediction and retrieval services.
Feature	Implementation
Framework	FastAPI 0.115.6
Authentication	JWT Bearer Token
Validation	Pydantic v2
CORS	Configurable origins
Rate Limiting	Future implementation
Key Endpoints
Method	Endpoint	Purpose
`POST`	`/api/v1/predict`	Analyze a customer support ticket
`POST`	`/api/v1/auth/signup`	Register a new user
`POST`	`/api/v1/auth/login`	Authenticate a user
`GET`	`/api/v1/metrics`	Retrieve system metrics
`GET`	`/api/v1/metrics/export`	Export prediction data
`POST`	`/api/v1/rag/retrieve`	Retrieve relevant FAQ solutions
---
2. ML Pipeline
The ML Pipeline is the core prediction component. It preprocesses incoming ticket text, extracts features, generates predictions, and integrates with the RAG service.
```text
┌──────────────────────────────────────────────────────────────┐
│                     PredictionPipeline                       │
│                                                              │
│ Input: title, description, resolution_time                   │
│                         │                                    │
│                         ▼                                    │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 1. Text Preprocessing                                    │ │
│ │    • Lowercasing                                         │ │
│ │    • Special character removal                           │ │
│ │    • Tokenization                                        │ │
│ │    • Stopword removal                                    │ │
│ │    • Lemmatization                                       │ │
│ └──────────────────────────────────────────────────────────┘ │
│                         │                                    │
│                         ▼                                    │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 2. Feature Extraction                                    │ │
│ │    • TF-IDF Vectorization                                │ │
│ │    • Advanced features (urgency, length, etc.)           │ │
│ └──────────────────────────────────────────────────────────┘ │
│                         │                                    │
│                         ▼                                    │
│        ┌──────────────┬──────────────┬──────────────┐        │
│        │   Category   │   Priority   │  Sentiment   │        │
│        │    97.12%    │    98.84%    │    89.58%    │        │
│        └──────────────┴──────────────┴──────────────┘        │
│                         │                                    │
│                         ▼                                    │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ 3. RAG Integration                                       │ │
│ │    • Query RAG service                                   │ │
│ │    • Retrieve relevant FAQs                              │ │
│ │    • Return suggested solution                            │ │
│ └──────────────────────────────────────────────────────────┘ │
│                         │                                    │
│                         ▼                                    │
│ Output: {category, priority, sentiment, solution}           │
└──────────────────────────────────────────────────────────────┘
```
Model Performance
Model	Accuracy
Category	97.12%
Priority	98.84%
Sentiment	89.58%
---
3. RAG Service
The RAG Service provides semantic search over the FAQ knowledge base.
It converts the user's query into an embedding, performs similarity search using FAISS, applies a similarity threshold, and returns the most relevant FAQ results.
```text
User Query
    │
    ▼
┌─────────────────────────────────────────────┐
│ 1. Embedding Generation                     │
│    Model: paraphrase-MiniLM-L3-v2           │
│    Output: 384-dimensional vector           │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│ 2. FAISS Similarity Search                  │
│    Index: IndexFlatIP                       │
│    Metric: Inner Product                    │
│    Results: Top 2                            │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│ 3. Threshold Filtering                      │
│    Threshold: 0.1                            │
└──────────────────────┬──────────────────────┘
                       ▼
        [{question, answer, similarity}]
```
Service Port: `8001`
Knowledge Base: `200 FAQs`
---
4. Monitoring Service
The Monitoring Service collects and stores prediction and error metrics.
```text
MetricsCollector
├── predictions: List[Dict]
├── errors: List[Dict]
├── start_time: datetime
├── storage_file: str
│
├── log_prediction()
├── get_summary()
├── get_user_tickets()
├── export_csv()
└── get_recent_tickets()
```
The service supports:
Prediction logging
Error tracking
Aggregated metrics
User-specific ticket history
CSV export
Recent prediction retrieval
---
5. Authentication Service
Authentication is implemented using JWT-based user management.
```text
                    Authentication Flow

1. SIGNUP
┌──────────┐       ┌────────────┐       ┌──────────────┐
│  Client  │ ────▶ │  /signup   │ ────▶ │ users.json   │
└──────────┘       └────────────┘       └──────────────┘

2. LOGIN
┌──────────┐       ┌────────────┐       ┌──────────────┐
│  Client  │ ────▶ │  /login    │ ────▶ │  JWT Token   │
└──────────┘       └────────────┘       └──────────────┘

3. AUTHENTICATED REQUEST
┌──────────┐       ┌────────────┐       ┌──────────────────┐
│  Client  │ ────▶ │   Bearer   │ ────▶ │ Protected        │
│          │       │   Token    │       │ Endpoint         │
└──────────┘       └────────────┘       └──────────────────┘
```
---
End-to-End Data Flow
Prediction Flow
```text
Client Request
{title, description, resolution_time, user_id}
        │
        ▼
┌─────────────────────────────────────────────┐
│ 1. API Gateway — /predict                   │
│    • Validate request using Pydantic        │
│    • Extract user_id                        │
│    • Start response-time timer              │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│ 2. ML Pipeline                              │
│    a. Preprocess text                       │
│    b. Extract features                      │
│    c. Predict category                      │
│    d. Predict priority                      │
│    e. Predict sentiment                     │
│    f. Apply rule-based overrides            │
│    g. Integrate with RAG                    │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│ 3. Monitoring Service                       │
│    • Log prediction metadata                │
│    • Calculate response time                │
│    • Store metrics in metrics_data.json     │
└──────────────────────┬──────────────────────┘
                       ▼
┌─────────────────────────────────────────────┐
│ 4. API Response                             │
│                                             │
│ {                                           │
│   category,                                 │
│   priority,                                 │
│   priority_confidence,                      │
│   sentiment,                                │
│   suggested_solution,                       │
│   source,                                   │
│   rag_confidence,                           │
│   rag_results                               │
│ }                                           │
└─────────────────────────────────────────────┘
```
---
Technology Stack
Backend
Component	Technology	Version
API Framework	FastAPI	0.115.6
ML Library	scikit-learn	1.6.1
NLP	NLTK	3.9.1
NLP / Embeddings	Sentence-Transformers	3.3.1
Vector Search	FAISS	1.9.0
Data Processing	Pandas	2.2.3
Numerical Computing	NumPy	1.26.4
Validation	Pydantic	2.10.4
Serialization	Joblib	1.4.2
Serialization	Pickle	—
HTTP Client	httpx	0.28.1
Logging	Loguru	0.7.3
Environment Management	python-dotenv	1.0.1
Frontend
Component	Technology	Version
Framework	Next.js	14.2.5
Language	TypeScript	5.x
Styling	Tailwind CSS	3.4.1
Icons	Lucide React	1.34.0
Infrastructure
Component	Technology
Containerization	Docker
Orchestration	Docker Compose
Backend Base Image	Python 3.11-slim
Frontend Base Image	Node 20-alpine
---
Security Architecture
The system uses multiple security layers.
1. Authentication
JWT (JSON Web Token)
Algorithm: `HS256`
Expiration: `24 hours` (configurable)
Payload: `{sub, email, role, exp}`
2. Authorization
Role-Based Access Control (RBAC) is used to restrict access according to user roles.
Role	Access
Admin	Full access, including dashboard and metrics
User	Prediction and personal history
3. Data Security
Passwords are stored using SHA-256 hashing
Plaintext passwords are not stored
User data is currently stored in a JSON file
Database encryption is planned as a future enhancement
4. API Security
Configurable CORS origins
Pydantic-based input validation
Rate limiting planned as a future enhancement
---
Monitoring & Observability
Metrics Collected
Metric	Description	Source
`total_predictions`	Total number of predictions	MetricsCollector
`uptime_hours`	Service uptime in hours	MetricsCollector
`priority_distribution`	Counts per priority	MetricsCollector
`sentiment_distribution`	Counts per sentiment class	MetricsCollector
`source_distribution`	FAQ vs. General sources	MetricsCollector
`avg_priority_confidence`	Average priority confidence score	MetricsCollector
`avg_rag_confidence`	Average RAG confidence score	MetricsCollector
`errors_count`	Number of errors	MetricsCollector
`response_time_ms`	API response time	API Middleware
Metrics Storage
Prediction and error data are persisted in `metrics_data.json`.
```text
metrics_data.json
├── predictions
│   ├── ticket_id
│   ├── user_id
│   ├── timestamp
│   ├── title
│   ├── description
│   ├── category
│   ├── priority
│   ├── sentiment
│   ├── suggested_solution
│   ├── source
│   ├── priority_confidence
│   ├── rag_confidence
│   ├── response_time_ms
│   └── user_feedback
│
├── errors
│   ├── timestamp
│   ├── error_id
│   ├── error_type
│   ├── error_message
│   └── context
│
└── metadata
    ├── start_time
    ├── last_updated
    ├── total_predictions
    ├── total_errors
    └── version
```
---
Scalability
Horizontal Scaling
Component	Scaling Strategy
API Gateway	Multiple instances behind a load balancer
RAG Service	Stateless and horizontally scalable
ML Pipeline	Stateless and horizontally scalable
Monitoring	Centralized with shared JSON storage; database planned
Authentication	Stateless JWT-based authentication
Vertical Scaling
Component	Resource Requirement
API Gateway	Low — 2 CPU, 2 GB RAM
RAG Service	Medium — 4 CPU, 8 GB RAM; FAISS in memory
ML Pipeline	Medium — 4 CPU, 4 GB RAM; model loading
Current Bottlenecks
FAISS index is stored in memory and therefore favors vertical scaling
JSON-based metrics storage is planned to migrate to PostgreSQL
Model loading time can be optimized using lazy loading
---
Deployment Architecture
The system is containerized using Docker Compose.
```text
Docker Compose
│
├── rag — Port 8001
│   ├── Base Image: Python 3.11-slim
│   ├── Sentence-Transformers
│   ├── FAISS
│   └── Entrypoint: run_rag.py
│
├── api — Port 8000
│   ├── Base Image: Python 3.11-slim
│   ├── FastAPI
│   ├── scikit-learn
│   └── Entrypoint: run.py
│
└── frontend — Port 3000
    ├── Base Image: Node 20-alpine
    ├── Next.js
    └── Entrypoint: npm start
```
Network
```text
customer-support-network (bridge)
```
Shared Volumes
```text
models/    # Shared model files
data/      # Shared application data
logs/      # Persistent logs
```
---
Future Enhancements
Enhancement	Description	Priority
Message Queue	Add Redis or RabbitMQ for asynchronous processing	High
Database	Migrate from JSON storage to PostgreSQL	High
Caching	Add Redis caching for RAG results	Medium
MLOps	Introduce MLflow for model versioning	Medium
Monitoring	Add Prometheus and Grafana	Medium
CI/CD	Automate workflows using GitHub Actions	Medium
Kubernetes	Support production-grade container orchestration	Low
A/B Testing	Enable controlled model experimentation	Low
---
Related Documentation
Backend Documentation
API Reference
Deployment Guide
Development Guide
---
Architecture Ownership
Eng. Aya Mohamed  
Lead ML Engineer & System Architect
---
<div align="center">
Customer Support AI  
System Architecture Documentation
Last Updated: August 2026
</div>