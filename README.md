# Social Media Content Generator API

## Objetivo del Proyecto

Esta aplicación es una **API REST construida con FastAPI** que permite generar contenido estructurado para redes sociales usando modelos de lenguaje (LLMs) de Azure OpenAI. El sistema almacena el contenido generado en una base de datos MySQL y proporciona endpoints CRUD para gestionar posts de redes sociales.

### Características principales:
- 🤖 Integración con Azure OpenAI para generación de contenido inteligente
- 📱 Soporte para múltiples plataformas (X, LinkedIn, Facebook, etc.)
- 💾 Persistencia en base de datos MySQL
- 🔧 Configuración flexible mediante archivos JSON
- 📚 API RESTful completa con operaciones CRUD
- 🎯 Generación de contenido con estilos personalizables (formal, informal, divertido)

---

## Instrucciones de Instalación y Ejecución

### Requisitos previos:
- Python 3.8 o superior
- MySQL Server instalado y en ejecución
- Credenciales de Azure OpenAI

### Pasos de instalación:

#### 1. Clonar o descargar el proyecto
```bash
cd path/to/proyecto
```

#### 2. Crear y activar el entorno virtual
```bash
# En Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# En Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. Configurar la base de datos MySQL

Crear la base de datos:
```sql
CREATE DATABASE social_media_db;
USE social_media_db;
```

#### 5. Configurar archivos de settings

**`settingsApp.json`** - Configuración de la aplicación y base de datos:
```json
{
  "database": {
    "host": "localhost",
    "user": "root",
    "password": "tu_contraseña",
    "database": "social_media_db",
    "port": 3306
  },
  "api": {
    "title": "Social Media Content Generator API",
    "version": "1.0.0",
    "description": "API para generar contenido estructurado para redes sociales usando LLMs"
  }
}
```

**`settingsLLM.json`** - Configuración de Azure OpenAI:
```json
{
  "openai": {
    "api_key": "tu_api_key_aqui",
    "endpoint": "https://tu-recurso.openai.azure.com/",
    "deployment_name": "tu_deployment_aqui",
    "api_version": "2024-02-15-preview"
  },
  "model_parameters": {
    "temperature": 0.7,
    "max_tokens": 1500,
    "top_p": 0.95,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
  }
}
```

#### 6. Ejecutar la aplicación
```bash
python m3_omar_pinzon.py
```

La API estará disponible en: `http://localhost:8000`

Para ver la documentación interactiva de Swagger: `http://localhost:8000/docs`

---

## Ejemplo de Uso

### 1. Obtener todos los posts
```bash
curl -X GET "http://localhost:8000/api/contents"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "platform": "X",
    "title": "Desarrollo con IA",
    "tone": "informal",
    "content": "Descubre cómo la IA está transformando el desarrollo...",
    "hashtags": "#IA #Desarrollo #Tech",
    "link": "https://ejemplo.com",
    "createdAt": "2024-02-14T10:30:00"
  }
]
```

### 2. Crear un post directamente
```bash
curl -X POST "http://localhost:8000/api/contents" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "LinkedIn",
    "title": "Transformación Digital",
    "tone": "formal",
    "content": "La transformación digital es clave en el mundo actual...",
    "hashtags": "#DigitalTransformation #Business",
    "link": "https://ejemplo.com"
  }'
```

### 3. Generar un post usando IA
```bash
curl -X POST "http://localhost:8000/api/contents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea un post motivacional sobre programación en Python para desarrolladores que están comenzando",
    "platform": "X"
  }'
```

**Respuesta:**
```json
{
  "id": 2,
  "platform": "X",
  "title": "Comienza tu viaje en Python",
  "tone": "informal",
  "content": "¡Hola! Si quieres aprender Python, este es el momento perfecto. Con constancia y práctica...",
  "hashtags": "#Python #Coding #Programacion",
  "link": null,
  "createdAt": "2024-02-14T10:35:00"
}
```

### 4. Obtener un post específico
```bash
curl -X GET "http://localhost:8000/api/contents/2"
```

### 5. Actualizar un post
```bash
curl -X PUT "http://localhost:8000/api/contents/2" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "X",
    "title": "Aprende Python hoy",
    "tone": "formal",
    "content": "Python es uno de los lenguajes más versátiles...",
    "hashtags": "#Python #Programming",
    "link": "https://python.org"
  }'
```

### 6. Eliminar un post
```bash
curl -X DELETE "http://localhost:8000/api/contents/2"
```

---

## Descripción de la Conexión a Base de Datos MySQL

### Arquitectura de conexión:

La aplicación utiliza **SQLAlchemy** como ORM para manejar la conexión a MySQL. La configuración se realiza mediante:

1. **Connection String**: Se construye a partir del archivo `settingsApp.json`
   ```
   mysql+mysqlconnector://usuario:contraseña@localhost:3306/social_media_db
   ```

2. **Modelo de datos**: La tabla `social_media_posts` se crea automáticamente en la primera ejecución

3. **Campos de la tabla**:
   | Campo | Tipo | Descripción |
   |-------|------|-------------|
   | `id` | INT PRIMARY KEY | Identificador único |
   | `platform` | VARCHAR(50) | Plataforma de red social |
   | `title` | VARCHAR(255) | Título o tema |
   | `tone` | VARCHAR(50) | Estilo (formal, informal, divertido) |
   | `content` | TEXT | Contenido del post |
   | `hashtags` | TEXT | Hashtags sugeridos |
   | `link` | VARCHAR(500) | Enlace externo |
   | `created_at` | DATETIME | Fecha de creación |

### Gestión de sesiones:

La aplicación usa un context manager `getDbSession()` que:
- Crea una nueva sesión para cada operación
- Realiza commit automático en caso de éxito
- Realiza rollback en caso de error
- Cierra la conexión automáticamente

### Ejemplo de query directo:
```python
with getDbSession() as session:
    posts = session.query(SocialMediaPostModel).filter(
        SocialMediaPostModel.platform == "X"
    ).all()
```

---

## Estructura del Proyecto

```
Actividad/
├── m3_omar_pinzon.py          # Aplicación principal FastAPI
├── requirements.txt            # Dependencias del proyecto
├── settingsApp.json            # Configuración de la app y BD
├── settingsLLM.json            # Configuración de Azure OpenAI
├── README.md                   # Documentación (este archivo)
├── .venv/                      # Entorno virtual
└── .git/                       # Control de versiones
```

---

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **Pydantic**: Validación de datos
- **MySQL**: Base de datos relacional
- **Azure OpenAI**: Generación de contenido con IA
- **Uvicorn**: Servidor ASGI

---

## Notas de Desarrollo

- El proyecto está tipado completamente para mayor seguridad
- La configuración se carga desde archivos JSON externos
- La API incluye manejo de errores y validaciones
- Se puede extender fácilmente con nuevos campos en los esquemas Pydantic

---

## Licencia

Uso académico - Actividad 3 - Programa Avanzado de IA
