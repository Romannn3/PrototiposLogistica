# Logistica Demo

Sistema de gestión de envíos y pedidos - Proyecto de demostración para portafolio.

## 🚀 Características Destacadas

### 📝 Parsing de Mensajes con Regex
Crea pedidos automáticamente desde mensajes de texto usando expresiones regulares.
```
📅 Día: hoy
👤 Cliente: Juan Pérez
📦 Productos: 
100 kg de Harina
50 litros de Aceite
📍 Lugar de entrega: Av. Siempreviva 742
```

### 📊 Importación/Exportación CSV
- Estrategia de procesamiento con streaming
- Vista previa antes de importar
- Exportación en tiempo real

### ⚠️ Alertas de Documentación
Dashboard con alertas automáticas de vencimiento (30 días) para:
- Licencias de conducir
- Seguros
- VTV y habilitaciones

## 🛠️ Stack Tecnológico

| Categoría | Tecnología |
|-----------|------------|
| Backend | Flask, SQLAlchemy, Flask-Login |
| Frontend | Jinja2, Bootstrap 5 |
| Testing | pytest, pytest-cov |
| CI/CD | GitHub Actions |
| Deploy | Vercel |


```

**Demo Login:** `admin` / `admin123`


```

## 📁 Estructura

```
app/
├── blueprints/         # Módulos (auth, pedidos, recursos, envios)
├── forms/              # WTForms
├── templates/          # Jinja2
├── static/             # CSS
├── models.py           # SQLAlchemy models
├── utils.py            # Regex parser, RBAC decorators
└── csv_handlers.py     # CSV Strategy pattern
tests/
├── test_parser.py      # Regex tests
├── test_routes.py      # Integration tests
└── test_csv.py         # CSV handler tests
```

## 🎯 Patrones Implementados

- **Application Factory Pattern** - Flask app creation
- **Blueprint Pattern** - Modular organization
- **Service Layer** - Business logic separation
- **Strategy Pattern** - CSV handlers
- **Factory Pattern** - CSV handler selection
- **Decorator Pattern** - RBAC (`@role_required`)

