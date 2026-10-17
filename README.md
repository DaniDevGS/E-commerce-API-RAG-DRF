# Ecommerce API RAG DRF

![Django](https://img.shields.io/badge/Django-5.2-092e20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776ab?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/AI-Groq%20%7C%20RAG-orange?style=for-the-badge)

![Swagger-UI](./Swagger%20UI%20portada.png)

Ecommerce-API-RAG-DRF is a robust backend system for eCommerce that integrates an intelligent virtual assistant (RAG Chatbot) capable of answering real-time inventory questions using semantic search and Large Language Models (LLMs).

## Description

Final project for the "API Development with Microservices Architecture" course. It demonstrates proficiency in Python, Django REST Framework, and AI model integration (LLM) via RAG (Retrieval-Augmented Generation). The chatbot **Techty** utilizes semantic search over a vector database to provide contextual responses about store products.

### Key Features

- Full **REST API** with JWT authentication
- **RAG Chatbot** featuring semantic product search
- Real-time **currency conversion** (USD -> VES)
- **Shopping cart** and order management system
- **Interactive documentation** with Swagger/Redoc
- **Rate limiting** and per-endpoint throttling

## Architecture

```mermaid
graph TD
    A[Root] --> B[core]
    A --> C[productos]
    A --> D[tienda]
    A --> E[usuarios]
    A --> F[chatbot]

    B --> B1[settings.py]
    B --> B2[urls.py]

    C --> C1[Product/Category Management]
    D --> D1[Cart and Purchase Orders]
    E --> E1[JWT User Management]
    F --> F1[AI Logic and RAG Vectors]

    F --> F2[Groq API / Llama.cpp]
    F --> F3[Upstash Vector DB]
```

- **core/**: Central configuration for the Django project
- **productos/**: Models and views for inventory, including currency conversion logic
- **tienda/**: Management of the purchasing workflow (Cart -> Order -> Stock)
- **usuarios/**: Custom authentication using SimpleJWT
- **chatbot/**: Integration with Groq/Llama.cpp and Upstash Vector for intelligent assistance

## Prerequisites

- **Python**: 3.10 or higher
- **pip**: Latest version
- **Venv**: Recommended for dependency isolation

Optional:
- **PostgreSQL** (if you prefer to use it instead of SQLite)
- **[Groq Account](https://console.groq.com)** (free, for the LLM)
- **[Upstash Account](https://console.upstash.com)** (free, for the vector database)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/DaniDevGS/Ecommerce-API-RAG-DRF.git
cd Ecommerce-API-RAG-DRF
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and update it with your credentials:

```bash
copy .env.example .env     # Windows
cp .env.example .env        # Linux/Mac
```

Open `.env` and set at least the minimum required variables:

```bash
SECRET_KEY=django-insecure-change-this-key
DEBUG=True
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Start the server

```bash
python manage.py runserver
```

The server will be available at `http://127.0.0.1:8000/`

## Environment Variables

The project works with a **minimal configuration** (only `SECRET_KEY` and `DEBUG`). Additional variables enable extra features.

### Required

| Variable | Description | Example |
| :--- | :--- | :--- |
| `SECRET_KEY` | Django secret key | `django-insecure-your-key` |
| `DEBUG` | Development mode | `True` |

### LLM (Choose your preferred provider)

| Variable | Description | Where to get it |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | Groq API Key (free) | [console.groq.com](https://console.groq.com) |
| `GROQ_API` | Groq Endpoint | `https://api.groq.com/openai/` |
| `LLAMACPP_API` | Local Llama.cpp Endpoint | `http://localhost:8080/` |

### Vector Database

| Variable | Description | Where to get it |
| :--- | :--- | :--- |
| `UPSTASH_VECTOR_REST_URL` | Upstash Vector URL | [console.upstash.com](https://console.upstash.com) |
| `UPSTASH_VECTOR_REST_TOKEN` | Upstash Vector Token | [console.upstash.com](https://console.upstash.com) |

### SQL Database (Optional)

| Variable | Description | Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql://user:pass@host:5432/db` |

### Minimal vs. Full Setup

#### MINIMAL - REST API Only

```bash
SECRET_KEY=your_key_here
DEBUG=True
```

#### WITH LLM - Chatbot responds without product context

```bash
SECRET_KEY=your_key_here
DEBUG=True
GROQ_API_KEY=gsk_your_key
GROQ_API=https://api.groq.com/openai/
```

#### FULL SETUP - Chatbot with semantic product search & REST API functionality

```bash
SECRET_KEY=your_key_here
DEBUG=True
GROQ_API_KEY=gsk_your_key
GROQ_API=https://api.groq.com/openai/
UPSTASH_VECTOR_REST_URL=https://your-vector.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your_token
```

## API Endpoints

| Method | Endpoint | Auth | Description |
| :--- | :--- | :---: | :--- |
| `GET` | `/` | No | Swagger UI (interactive documentation) |
| `POST` | `/api/auth/login/` | No | Login and obtain JWT |
| `POST` | `/api/auth/refresh/` | No | Refresh JWT token |
| `POST` | `/api/usuario/` | No | Register user |
| `GET` | `/api/usuario/` | Admin | List users |
| `GET` | `/api/productos/` | No | List/filter products |
| `GET` | `/api/productos/<id>/` | No | Product details |
| `GET` | `/api/categorias/` | No | List categories |
| `GET` | `/api/subcategorias/` | No | List subcategories |
| `GET` | `/api/carritos/` | JWT | View my cart |
| `POST` | `/api/items-carrito/` | JWT | Add item to cart |
| `PATCH` | `/api/items-carrito/<id>/` | JWT | Edit cart item |
| `DELETE` | `/api/items-carrito/<id>/` | JWT | Delete cart item |
| `POST` | `/api/ordenes-compra/` | JWT | Create order from cart |
| `GET` | `/api/ordenes-compra/` | JWT | List my orders |
| `POST` | `/api/chatbot/` | JWT | Query chatbot (RAG) |
| `GET` | `/api/chatbot/` | JWT | View chat history |

### Example: Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Example: Querying the Chatbot

```bash
curl -X POST http://127.0.0.1:8000/api/chatbot/ \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{"pregunta": "What laptops do you have available?"}'
```

## Project Structure

```
backend/
├── core/                # Django Configuration (settings, urls, wsgi)
├── productos/          # Models: Category, Subcategory, Product
├── tienda/              # Models: Cart, CartItem, PurchaseOrder
├── usuarios/            # User Management with JWT
├── chatbot/             # RAG: rag.py (LLM), vectors.py (Upstash)
├── media/               # Uploaded media files
├── requirements.txt    # Python Dependencies
├── .env_example        # Environment variables template
└── manage.py            # Django management commands
```

## Technologies

| Component | Technology | Version |
| :--- | :--- | :--- |
| Framework | Django | 5.2 |
| REST API | Django REST Framework | 3.16 |

## License

This project is licensed under **Personal Use Only**. Distribution, sale, or usage in production environments is strictly prohibited. Refer to the [LICENSE](./LICENSE) file for details.
