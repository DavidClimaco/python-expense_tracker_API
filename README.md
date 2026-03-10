# Expense Tracker API

API REST para el seguimiento de gastos personales, desarrollada con **Python** y **FastAPI**.

## Descripción del Proyecto

Expense Tracker API es una aplicación backend que permite a los usuarios registrar, gestionar y consultar sus gastos personales de manera segura. La API implementa autenticación JWT y persiste los datos en una base de datos PostgreSQL.

### Características Principales

- **Gestión de Usuarios**: Registro, actualización y eliminación de usuarios
- **Autenticación Segura**: Login con tokens JWT (validez de 30 minutos)
- **Gestión de Gastos**: CRUD completo de gastos (crear, leer, actualizar, eliminar)
- **Categorías de Gastos**: Groceries, Leisure, Electronics, Utilities, Clothing, Health, Others
- **Seguridad**: Contraseñas hasheadas con Argon2

## Arquitectura del Proyecto

```
03_expense_tracker_API/
├── app/
│   ├── config/
│   │   ├── config_env.py      # Configuración de variables de entorno
│   │   ├── db.py              # Configuración de la base de datos
│   │   └── security.py        # Seguridad (JWT, hashing de contraseñas)
│   ├── models/
│   │   ├── expense_model.py   # Modelo de datos para gastos
│   │   └── user_model.py      # Modelo de datos para usuarios
│   ├── routers/
│   │   ├── auth_router.py     # Endpoints de autenticación
│   │   ├── expenses_router.py # Endpoints de gestión de gastos
│   │   └── user_router.py     # Endpoints de gestión de usuarios
│   ├── test/
│   │   ├── conftest.py        # Configuración de pruebas
│   │   ├── test_auth.py       # Pruebas de autenticación
│   │   ├── test_expenses.py   # Pruebas de gastos
│   │   └── test_user.py       # Pruebas de usuarios
│   └── main.py                # Punto de entrada de la aplicación
├── docker-compose.yaml        # Configuración de PostgreSQL
├── pyproject.toml             # Dependencias del proyecto
└── .env                       # Variables de entorno
```

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLModel**: ORM para la gestión de la base de datos
- **PostgreSQL**: Sistema de gestión de base de datos relacional
- **PyJWT**: Generación y validación de tokens JWT
- **pwdlib**: Biblioteca para hashing de contraseñas (Argon2)
- **pytest**: Framework para pruebas

## Endpoints de la API

### Autenticación

| Método | Endpoint      | Descripción                    |
|--------|---------------|--------------------------------|
| POST   | `/login`      | Inicio de sesión (retorna JWT) |
| POST   | `/logout`     | Cierre de sesión               |

### Usuarios

| Método | Endpoint           | Descripción                   |
|--------|--------------------|-------------------------------|
| POST   | `/register`       | Registrar nuevo usuario       |
| PATCH  | `/register/{id}`  | Actualizar usuario            |
| DELETE | `/register/{id}`  | Eliminar usuario              |

### Gastos

| Método | Endpoint            | Descripción                     |
|--------|---------------------|---------------------------------|
| GET    | `/expenses`        | Listar todos los gastos         |
| GET    | `/expenses/{id}`   | Obtener un gasto específico    |
| POST   | `/expenses`        | Crear nuevo gasto              |
| PATCH  | `/expenses/{id}`   | Actualizar un gasto            |
| DELETE | `/expenses/{id}`   | Eliminar un gasto              |

## Pasos para Ejecutar el Proyecto

### Prerrequisitos

- Python 3.13+
- Docker y Docker Compose (para PostgreSQL)

### 1. Clonar el Repositorio

```bash
git clone <repositorio>
cd 03_expense_tracker_API
```

### 2. Configurar Variables de Entorno

Crea un archivo `.env` basado en el ejemplo `.env.example`:

```env
DATABASE_USER=postgres
DATABASE_PASSWORD=tu_password
DATABASE_NAME=expense_tracker
DATABASE_HOST=localhost
DATABASE_PORT=5432

SECRET_KEY=tu_secret_key_aqui
ALGORITHM=HS256
```

### 3. Iniciar la Base de Datos

```bash
docker-compose up -d
```

### 4. Instalar Dependencias

```bash
pip install -e .
```

O si usas `uv`:

```bash
uv sync
```

### 5. Ejecutar el Servidor

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

### 6. Documentación Interactiva

FastAPI genera documentación automática:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Ejemplo de Uso

### 1. Registrar un Usuario

```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@correo.com", "password": "password123", "name": "Juan"}'
```

### 2. Iniciar Sesión

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@correo.com&password=password123"
```

### 3. Crear un Gasto (con token JWT)

```bash
curl -X POST "http://localhost:8000/expenses" \
  -H "Authorization: Bearer <tu_token_jwt>" \
  -H "Content-Type: application/json" \
  -d '{"ammount": 50.00, "category": "groceries", "description": "Compra semanal"}'
```

### 4. Listar Gastos

```bash
curl -X GET "http://localhost:8000/expenses" \
  -H "Authorization: Bearer <tu_token_jwt>"
```

## Ejecución de Pruebas

```bash
pytest
```

## Licencia

MIT
