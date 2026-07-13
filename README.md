# Ecommerce API RAG DRF

![Django](https://img.shields.io/badge/Django-5.2-092e20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.16-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776ab?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/AI-Groq%20%7C%20RAG-orange?style=for-the-badge)

![Swagger-UI](./Swagger%20UI%20portada.png)

Ecommerce-API-RAG-DRF es un sistema backend robusto para eCommerce que integra un asistente virtual inteligente (Chatbot RAG) capaz de responder preguntas sobre el inventario en tiempo real utilizando búsqueda semántica y modelos de lenguaje grandes.

## Descripcion

Proyecto de finalizacion del curso de "Desarrollo de APIs con arquitectura de Microservicios". Demuestra dominio de Python, Django Rest Framework e integracion con modelos de IA (LLM) mediante RAG (Retrieval-Augmented Generation). El chatbot **Techty** usa busqueda semántica sobre una base de datos vectorial para dar respuestas contextuales sobre los productos de la tienda.

### Caracteristicas principales

- **API REST** completa con autenticacion JWT
- **Chatbot RAG** con busqueda semantica de productos
- **Conversion de divisas** en tiempo real (USD -> VES)
- **Carrito de compras** y sistema de ordenes
- **Documentacion interactiva** con Swagger/Redoc
- **Rate limiting** y throttling por endpoint

## Arquitectura

```mermaid
graph TD
    A[Root] --> B[core]
    A --> C[productos]
    A --> D[tienda]
    A --> E[usuarios]
    A --> F[chatbot]

    B --> B1[settings.py]
    B --> B2[urls.py]

    C --> C1[Gestion de Productos/Categorias]
    D --> D1[Carrito y Ordenes de Compra]
    E --> E1[Gestion de Usuarios JWT]
    F --> F1[Logica de IA y Vectores RAG]

    F --> F2[Groq API / Llama.cpp]
    F --> F3[Upstash Vector DB]
```

- **core/**: Configuracion central del proyecto Django
- **productos/**: Modelos y vistas para el inventario, incluyen logica de conversion de divisas
- **tienda/**: Gestion del flujo de compra (Carrito -> Orden -> Stock)
- **usuarios/**: Autenticacion personalizada con SimpleJWT
- **chatbot/**: Integracion con Groq/Llama.cpp y Upstash Vector para asistencia inteligente

## Requisitos Previos

- **Python**: 3.10 o superior
- **pip**: Ultima version
- **Venv**: Recomendado para aislamiento de dependencias

Opcionales:
- **PostgreSQL** (si deseas usar en lugar de SQLite)
- **Cuenta en [Groq](https://console.groq.com)** (gratis, para el LLM)
- **Cuenta en [Upstash](https://console.upstash.com)** (gratis, para la base de datos vectorial)

## Instalacion

### 1. Clonar el repositorio

```bash
git clone https://github.com/DaniDevGS/Ecommerce-API-RAG-DRF.git
cd Ecommerce-API-RAG-DRF
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y editalo con tus credenciales:

```bash
copy .env.example .env     # Windows
cp .env.example .env       # Linux/Mac
```

Abre `.env` y configura al menos las variables minimas:

```bash
SECRET_KEY=django-insecure-cambia-esta-clave
DEBUG=True
```

### 5. Ejecutar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

El servidor estara disponible en `http://127.0.0.1:8000/`

## Variables de Entorno

El proyecto funciona con **configuracion minima** (solo `SECRET_KEY` y `DEBUG`). Las variables adicionales habilitan funcionalidades extra.

### Requeridas

| Variable | Descripcion | Ejemplo |
| :--- | :--- | :--- |
| `SECRET_KEY` | Llave secreta de Django | `django-insecure-tu-clave` |
| `DEBUG` | Modo desarrollo | `True` |

### LLM (Elige la que quieras)

| Variable | Descripcion | Donde obtenerla |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | API Key de Groq (gratis) | [console.groq.com](https://console.groq.com) |
| `GROQ_API` | Endpoint de Groq | `https://api.groq.com/openai/` |
| `LLAMACPP_API` | Endpoint de Llama.cpp local | `http://localhost:8080/` |

### Base de datos vectorial

| Variable | Descripcion | Donde obtenerla |
| :--- | :--- | :--- |
| `UPSTASH_VECTOR_REST_URL` | URL de Upstash Vector | [console.upstash.com](https://console.upstash.com) |
| `UPSTASH_VECTOR_REST_TOKEN` | Token de Upstash Vector | [console.upstash.com](https://console.upstash.com) |

### Base de datos SQL (Opcional)

| Variable | Descripcion | Ejemplo |
| :--- | :--- | :--- |
| `DATABASE_URL` | URL de conexion PostgreSQL | `postgresql://user:pass@host:5432/db` |

### Configuracion minima vs completa

#### MINIMA - Solo API REST 

```bash
SECRET_KEY=tu_clave_aqui
DEBUG=True
```

#### CON LLM - Chatbot responde pero sin contexto de productos

```bash
SECRET_KEY=tu_clave_aqui
DEBUG=True
GROQ_API_KEY=gsk_tu_key
GROQ_API=https://api.groq.com/openai/
```

#### COMPLETA - Chatbot con busqueda semantica de productos y funcionalidad de API REST

```bash
SECRET_KEY=tu_clave_aqui
DEBUG=True
GROQ_API_KEY=gsk_tu_key
GROQ_API=https://api.groq.com/openai/
UPSTASH_VECTOR_REST_URL=https://tu-vector.upstash.io
UPSTASH_VECTOR_REST_TOKEN=tu_token
```

## Endpoints API

| Metodo | Endpoint | Auth | Descripcion |
| :--- | :--- | :---: | :--- |
| `GET` | `/` | No | Swagger UI (documentacion interactiva) |
| `POST` | `/api/auth/login/` | No | Login y obtener JWT |
| `POST` | `/api/auth/refresh/` | No | Refrescar token JWT |
| `POST` | `/api/usuario/` | No | Registrar usuario |
| `GET` | `/api/usuario/` | Admin | Listar usuarios |
| `GET` | `/api/productos/` | No | Listar/filtrar productos |
| `GET` | `/api/productos/<id>/` | No | Detalle de producto |
| `GET` | `/api/categorias/` | No | Listar categorias |
| `GET` | `/api/subcategorias/` | No | Listar subcategorias |
| `GET` | `/api/carritos/` | JWT | Ver mi carrito |
| `POST` | `/api/items-carrito/` | JWT | Agregar item al carrito |
| `PATCH` | `/api/items-carrito/<id>/` | JWT | Editar item del carrito |
| `DELETE` | `/api/items-carrito/<id>/` | JWT | Eliminar item del carrito |
| `POST` | `/api/ordenes-compra/` | JWT | Crear orden desde el carrito |
| `GET` | `/api/ordenes-compra/` | JWT | Listar mis ordenes |
| `POST` | `/api/chatbot/` | JWT | Preguntar al chatbot (RAG) |
| `GET` | `/api/chatbot/` | JWT | Ver historial de chat |

### Ejemplo: Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "tu_usuario", "password": "tu_password"}'
```

### Ejemplo: Preguntar al chatbot

```bash
curl -X POST http://127.0.0.1:8000/api/chatbot/ \
  -H "Authorization: Bearer tu_token_jwt" \
  -H "Content-Type: application/json" \
  -d '{"pregunta": "Que laptops tienen disponibles?"}'
```

## Estructura del Proyecto

```
backend/
├── core/               # Configuracion Django (settings, urls, wsgi)
├── productos/          # Modelos: Categoria, Subcategoria, Producto
├── tienda/             # Modelos: Carrito, ItemCarrito, OrdenCompra
├── usuarios/           # Gestion de usuarios con JWT
├── chatbot/            # RAG: rag.py (LLM), vectors.py (Upstash)
├── media/              # Archivos multimedia subidos
├── requirements.txt    # Dependencias Python
├── .env_example        # Template de variables de entorno
└── manage.py           # Comandos de Django
```

## Tecnologias

| Componente | Tecnologia | Version |
| :--- | :--- | :--- |
| Framework | Django | 5.2 |
| API REST | Django REST Framework | 3.16 |

## Licencia

Este proyecto esta bajo la licencia de **Uso Personal Unicamente**. No esta permitida la distribucion, venta o uso en entornos de produccion. Consulta el archivo [LICENSE](./LICENSE) para mas detalles.