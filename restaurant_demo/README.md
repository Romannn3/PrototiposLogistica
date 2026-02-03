# Restaurant Manager - Flask Demo Project

Sistema de gestión de restaurante desarrollado con Flask, demostrando buenas prácticas y patrones de diseño modernos.

## 🚀 Tecnologías

| Categoría | Tecnologías |
|-----------|-------------|
| **Backend** | Python 3.11, Flask 3.x, SQLAlchemy 2.0, Flask-Migrate |
| **Auth** | Flask-Login, Flask-Bcrypt, RBAC con decoradores |
| **Forms** | Flask-WTF, WTForms, CSRF Protection |
| **Database** | SQLite (dev), PostgreSQL (prod) |
| **Frontend** | Bootstrap 5, Jinja2 Templates |
| **Testing** | pytest, pytest-cov, pytest-flask |
| **CI/CD** | GitHub Actions, Codecov |
| **Deploy** | Vercel (serverless) |

## 🏗️ Arquitectura

```
app/
├── __init__.py          # Application Factory Pattern
├── models.py            # SQLAlchemy Models
├── utils.py             # Decorators & Helpers
├── forms/               # WTForms
├── blueprints/          # Modular Blueprints
│   ├── auth/           # Authentication
│   ├── menu/           # Menu Management
│   └── pedidos/        # Order Management
├── templates/           # Jinja2 Templates
└── static/              # CSS, JS, Images
```

## 📦 Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd restaurant_demo

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Inicializar base de datos
python setup_db.py

# Ejecutar aplicación
python run.py
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html
```

## 🔐 Credenciales Demo

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | Administrador |
| mozo1 | mozo123 | Mozo |

## 📋 Funcionalidades

- ✅ Autenticación con roles (admin, mozo, cocinero)
- ✅ Gestión de menú (CRUD de platos y categorías)
- ✅ Gestión de pedidos por mesa
- ✅ Estados de pedido con flujo de trabajo
- ✅ Dashboard con métricas del día
- ✅ Diseño responsive con Bootstrap 5

## 🔧 Patrones Implementados

- **Application Factory** - Configuración flexible
- **Blueprints** - Modularización por dominio
- **Service Layer** - Separación de lógica de negocio
- **RBAC** - Control de acceso basado en roles
- **Repository Pattern** - Abstracción de datos

## 📄 Licencia

MIT License - Proyecto de demostración para portafolio.
