# Social Media Content Generator API

## 📋 Tabla de Contenidos
1. [Objetivo del Proyecto](#objetivo-del-proyecto)
2. [Características Principales](#características-principales)
3. [Guía de Inicio Rápido](#guía-de-inicio-rápido)
4. [Instrucciones Completas de Instalación](#instrucciones-completas-de-instalación)
5. [Configuración de la Base de Datos MySQL](#configuración-de-la-base-de-datos-mysql)
6. [Ejemplos de Uso de la API](#ejemplos-de-uso-de-la-api)
7. [Referencia Completa de Endpoints](#referencia-completa-de-endpoints)
8. [Aclaraciones sobre Swagger/OpenAPI](#aclaraciones-sobre-swaggeropenapi)
9. [Estructura del Proyecto](#estructura-del-proyecto)
10. [Tecnologías Utilizadas](#tecnologías-utilizadas)
11. [Solución de Problemas](#solución-de-problemas)

---

## Objetivo del Proyecto

Esta aplicación es una **API REST construida con FastAPI** que permite generar contenido estructurado para redes sociales usando modelos de lenguaje (LLMs) de Azure OpenAI. El sistema almacena el contenido generado en una base de datos MySQL y proporciona endpoints CRUD completos para gestionar posts de redes sociales.

### Características principales:
- 🤖 Integración con Azure OpenAI para generación de contenido inteligente
- 📱 Soporte para múltiples plataformas (X, LinkedIn, Facebook, Instagram, TikTok, etc.)
- 💾 Persistencia en base de datos MySQL
- 🔧 Configuración flexible mediante archivos JSON
- 📚 API RESTful completa con operaciones CRUD
- 🎯 Generación de contenido con estilos personalizables (formal, informal, divertido)
- ✨ Tipado completo de datos con Pydantic v2
- 📖 Documentación interactiva con Swagger/OpenAPI

---

# 🚀 Guía de Inicio Rápido

## Requisitos previos
- **Python 3.8+** instalado
- **MySQL Server** en ejecución
- **Credenciales de Azure OpenAI** (para la generación con IA)

---

## ⚡ Pasos rápidos para empezar

### 1️⃣ Preparar la base de datos (IMPORTANTE)

**Solo necesitas crear la base de datos. La tabla se crea automáticamente.**

```sql
-- Ejecuta SOLO esto en MySQL:
CREATE DATABASE social_media_db;
```

La tabla `social_media_posts` se creará automáticamente cuando ejecutes la aplicación.

### 2️⃣ Configurar las credenciales

Edita `settingsApp.json` con tus credenciales de MySQL:
```json
{
  "database": {
    "host": "localhost",
    "user": "root",
    "password": "TU_CONTRASEÑA",
    "database": "social_media_db",
    "port": 3306
  }
}
```

Edita `settingsLLM.json` con tus credenciales de Azure OpenAI:
```json
{
  "openai": {
    "api_key": "tu-api-key-aqui",
    "endpoint": "https://tu-recurso.openai.azure.com/",
    "deployment_name": "tu-deployment-aqui"
  }
}
```

### 3️⃣ Instalar dependencias (primera vez)

```bash
# Windows
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Linux/Mac
source .venv/bin/activate
pip install -r requirements.txt
```

### 4️⃣ Ejecutar la aplicación

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
bash run.sh
```

**O manualmente:**
```bash
python m3_omar_pinzon.py
```

### 5️⃣ Acceder a la API

- **API URL**: http://localhost:8000
- **Documentación interactiva**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📝 Ejemplos rápidos

### Crear un post (sin IA)

```bash
curl -X POST "http://localhost:8000/api/contents" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "X",
    "title": "Mi primer post",
    "tone": "informal",
    "content": "¡Hola mundo!",
    "hashtags": "#primero",
    "link": "https://ejemplo.com"
  }'
```

### Generar un post con IA

```bash
# Para X (sin especificar plataforma)
curl -X POST "http://localhost:8000/api/contents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea un tweet sobre inteligencia artificial"
  }'

# Para LinkedIn (especifica la plataforma en el prompt)
curl -X POST "http://localhost:8000/api/contents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea un post profesional para LinkedIn sobre programación en Python"
  }'

# Para Facebook (especifica la plataforma en el prompt)
curl -X POST "http://localhost:8000/api/contents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea un post amigable para Facebook con consejos sobre desarrollo web"
  }'
```

**Nota importante**: Solo se requiere el `prompt`. Si no especificas plataforma en el prompt, usa "X" como defecto.

### Obtener todos los posts

```bash
curl -X GET "http://localhost:8000/api/contents"
```

---

## 🧪 Ejecutar tests

```bash
.\.venv\Scripts\pytest test_m3_omar_pinzon.py -v
```

---

## 📋 Verificación de requisitos

Para verificar que todo está configurado correctamente:

```powershell
# Verificar Python
python --version

# Verificar MySQL (desde otra terminal)
mysql -u root -p

# Verificar que MySQL puede conectarse
mysql -u root -p social_media_db -e "SELECT 1;"
```

---

# Instrucciones Completas de Instalación

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

**IMPORTANTE**: Solo debes crear la base de datos manualmente. La tabla se crea **automáticamente** en la primera ejecución.

```sql
-- Ejecuta SOLO esto en MySQL:
CREATE DATABASE social_media_db;
```

La tabla `social_media_posts` se creará automáticamente cuando ejecutes la aplicación por primera vez, con la siguiente estructura:

```sql
CREATE TABLE social_media_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    tone VARCHAR(50),
    content LONGTEXT,
    hashtags TEXT,
    link VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Nota**: Esta tabla se genera automáticamente por SQLAlchemy. No necesitas ejecutar el comando CREATE TABLE manualmente.

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
    "deployment_name": "tu_deployment_aqui"
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

# Configuración de la Base de Datos MySQL

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

# Ejemplos de Uso de la API REST

## 1. Health Check - Verificar que la API está funcionando

```bash
curl -X GET "http://localhost:8000/" \
  -H "Content-Type: application/json"
```

Respuesta esperada:
```json
{
  "message": "Social Media Content Generator API",
  "version": "1.0.0",
  "status": "running"
}
```

---

## 2. Obtener todos los posts de redes sociales

```bash
curl -X GET "http://localhost:8000/api/contents" \
  -H "Content-Type: application/json"
```

Respuesta esperada:
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

---

## 3. Crear un post manualmente (sin IA)

```bash
curl -X POST "http://localhost:8000/api/contents" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "LinkedIn",
    "title": "Transformación Digital",
    "tone": "formal",
    "content": "La transformación digital es fundamental para el éxito en el mundo actual. Las empresas que adapten sus procesos y estrategias tecnológicas estarán mejor posicionadas para competir.",
    "hashtags": "#DigitalTransformation #Business #Technology",
    "link": "https://ejemplo.com/articulo"
  }'
```

Respuesta esperada:
```json
{
  "id": 2,
  "platform": "LinkedIn",
  "title": "Transformación Digital",
  "tone": "formal",
  "content": "La transformación digital es fundamental...",
  "hashtags": "#DigitalTransformation #Business #Technology",
  "link": "https://ejemplo.com/articulo",
  "createdAt": "2024-02-14T10:35:00"
}
```

---

## 4. Generar un post usando IA (Azure OpenAI)

**Nota importante:** Este endpoint requiere que:
1. Tengas credenciales válidas de Azure OpenAI en `settingsLLM.json`
2. El archivo `settingsLLM.json` esté correctamente configurado
3. La plataforma se especifique **dentro del prompt** - el LLM la identificará automáticamente

### Ejemplo 1: Generar post para X (por defecto)
```bash
curl -X POST "http://localhost:8000/api/contents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea un post motivacional sobre aprender programación en Python. Debe ser dirigido a desarrolladores principiantes, inspirador y práctico."
  }'
```

### Ejemplo 2: Generar post para LinkedIn (plataforma especificada en prompt)
```bash
curl -X POST "http://localhost:8000/api/contents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea un post profesional para LinkedIn sobre transformación digital en empresas modernas. Debe ser formal, informativo y motivador."
  }'
```

### Ejemplo 3: Generar post para Facebook
```bash
curl -X POST "http://localhost:8000/api/contents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea un post amigable para Facebook sobre consejos de programación para principiantes. Incluye emojis y un tono casual."
  }'
```

Respuesta esperada:
```json
{
  "id": 3,
  "platform": "LinkedIn",
  "title": "Transformación Digital en Empresas",
  "tone": "formal",
  "content": "La transformación digital es una realidad en el mundo empresarial actual. Las organizaciones que adopten tecnologías modernas y paradigmas ágiles estarán mejor posicionadas para competir en el mercado...",
  "hashtags": "#TransformacionDigital #Empresa #Tecnologia",
  "link": "https://resources.example.com/transformacion-digital-xyz",
  "createdAt": "2024-02-14T10:40:00"
}
```

---

## 5. Obtener un post específico por su ID

```bash
curl -X GET "http://localhost:8000/api/contents/2" \
  -H "Content-Type: application/json"
```

---

## 6. Actualizar un post existente

```bash
curl -X PUT "http://localhost:8000/api/contents/2" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "X",
    "title": "Aprende Python Hoy",
    "tone": "formal",
    "content": "Python es uno de los lenguajes de programación más versátiles y ampliamente utilizado en la industria actualmente.",
    "hashtags": "#Python #Programming #Development",
    "link": "https://python.org"
  }'
```

---

## 7. Eliminar un post

```bash
curl -X DELETE "http://localhost:8000/api/contents/2" \
  -H "Content-Type: application/json"
```

Respuesta esperada:
```json
{
  "message": "Post con ID 2 eliminado exitosamente"
}
```

---

## Ejemplos adicionales con Python requests

Si prefieres usar Python en lugar de curl:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Obtener todos los posts
response = requests.get(f"{BASE_URL}/api/contents")
print(response.json())

# 2. Crear un post
newPost = {
    "platform": "Facebook",
    "title": "Mi primer post",
    "tone": "informal",
    "content": "¡Hola a todos! Este es mi primer post en la API.",
    "hashtags": "#primero #api #socialmedia"
}
response = requests.post(f"{BASE_URL}/api/contents", json=newPost)
print(response.json())

# 3. Generar contenido con IA (solo prompt requerido)
generateRequest = {
    "prompt": "Escribe un post educativo sobre machine learning"
}
response = requests.post(f"{BASE_URL}/api/contents/generate", json=generateRequest)
print(response.json())

# 3b. Generar con plataforma específica (opcional)
generateRequest2 = {
    "prompt": "Escribe un post sobre transformación digital",
    "platform": "LinkedIn"
}
response = requests.post(f"{BASE_URL}/api/contents/generate", json=generateRequest2)
print(response.json())

# 4. Actualizar un post
updatedPost = {
    "platform": "X",
    "title": "Post actualizado",
    "tone": "formal",
    "content": "Contenido del post actualizado",
    "hashtags": "#actualizado"
}
response = requests.put(f"{BASE_URL}/api/contents/1", json=updatedPost)
print(response.json())

# 5. Eliminar un post
response = requests.delete(f"{BASE_URL}/api/contents/1")
print(response.json())
```

---

# Referencia Completa de Endpoints

## ✅ Estado actual de los endpoints

### 1. **GET / - Health Check**
Verifica que la API está funcionando.
```bash
curl -X GET "http://localhost:8000/"
```

---

### 2. **GET /api/contents**
Obtiene todos los posts.
```bash
curl -X GET "http://localhost:8000/api/contents"
```

---

### 3. **GET /api/contents/{id}**
Obtiene un post específico por ID.
```bash
curl -X GET "http://localhost:8000/api/contents/1"
```

---

### 4. **POST /api/contents**
Crea un post manualmente (CRUD directo).

**Campos requeridos:**
- `platform` ✅ Requerido
- `title` ✅ Requerido
- `tone` ✅ Requerido
- `content` ✅ Requerido

**Campos opcionales:**
- `hashtags` (opcional)
- `link` (opcional)

```bash
curl -X POST "http://localhost:8000/api/contents" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "X",
    "title": "Mi primer post",
    "tone": "informal",
    "content": "¡Hola mundo!",
    "hashtags": "#primera",
    "link": "https://ejemplo.com"
  }'
```

---

### 5. **POST /api/contents/generate** ⭐
Genera un post usando IA. La plataforma se especifica **dentro del prompt**.

**Campos requeridos:**
- `prompt` ✅ Requerido (describe qué quieres y para qué plataforma)

**Nota importante:** El LLM analizará tu prompt para identificar la plataforma. Si no especificas una, usará "X" por defecto.

#### Ejemplo 1: Para X (sin especificar plataforma)
```bash
curl -X POST "http://localhost:8000/api/contents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea un tweet motivacional sobre aprender programación"
  }'
```

#### Ejemplo 2: Para LinkedIn (plataforma en el prompt)
```bash
curl -X POST "http://localhost:8000/api/contents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea un post profesional para LinkedIn sobre transformación digital en empresas"
  }'
```

#### Ejemplo 3: Para Facebook (plataforma en el prompt)
```bash
curl -X POST "http://localhost:8000/api/contents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea un post amigable para Facebook con consejos de programación para principiantes"
  }'
```

#### Respuesta esperada:
```json
{
  "id": 5,
  "platform": "LinkedIn",
  "title": "Transformación Digital en Empresas",
  "tone": "formal",
  "content": "La transformación digital es fundamental para el éxito empresarial...",
  "hashtags": "#TransformacionDigital #Empresa #Tech",
  "link": "https://resources.example.com/transformacion-digital-xyz",
  "createdAt": "2024-02-14T10:45:00"
}
```

---

### 6. **PUT /api/contents/{id}**
Actualiza un post existente.

**Campos requeridos (igual que POST /api/contents):**
- `platform` ✅ Requerido
- `title` ✅ Requerido
- `tone` ✅ Requerido
- `content` ✅ Requerido

```bash
curl -X PUT "http://localhost:8000/api/contents/1" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "LinkedIn",
    "title": "Título actualizado",
    "tone": "formal",
    "content": "Contenido actualizado",
    "hashtags": "#actualizado",
    "link": "https://actual.com"
  }'
```

---

### 7. **DELETE /api/contents/{id}**
Elimina un post por ID.

```bash
curl -X DELETE "http://localhost:8000/api/contents/1"
```

---

## 🎯 Comparación: POST /api/contents vs POST /api/contents/generate

| Campo | /api/contents | /api/contents/generate |
|-------|---------------|----------------------|
| `platform` | ✅ Requerido | ❌ No necesario (lo identifica IA del prompt) |
| `title` | ✅ Requerido | ❌ No necesario (lo genera IA) |
| `tone` | ✅ Requerido | ❌ No necesario (lo genera IA) |
| `content` | ✅ Requerido | ❌ No necesario (lo genera IA) |
| `hashtags` | ⭐ Opcional | ❌ No necesario (lo genera IA) |
| `link` | ⭐ Opcional | ❌ No necesario (lo genera IA) |
| `prompt` | ❌ No existe | ✅ Requerido (describe qué y para dónde) |

---

## 📝 Ejemplos completos en Python

```python
import requests

BASE_URL = "http://localhost:8000"

# ====== GENERATE ENDPOINT - NUEVO COMPORTAMIENTO ======
# La plataforma se especifica EN EL PROMPT
# El LLM la identifica automáticamente

# Ejemplo 1: Para X (no especificas plataforma, usa X por defecto)
response = requests.post(
    f"{BASE_URL}/api/contents/generate",
    json={"prompt": "Crea un tweet divertido sobre debugging"}
)
print("Tweet para X:", response.json())

# Ejemplo 2: Para LinkedIn (especificas plataforma en el prompt)
response = requests.post(
    f"{BASE_URL}/api/contents/generate",
    json={"prompt": "Crea un post profesional para LinkedIn sobre liderazgo en tecnología"}
)
print("Post LinkedIn:", response.json())

# Ejemplo 3: Para Facebook (especificas plataforma en el prompt)
response = requests.post(
    f"{BASE_URL}/api/contents/generate",
    json={"prompt": "Crea un post amigable para Facebook con tips de programación para principiantes"}
)
print("Post Facebook:", response.json())

# ====== CREATE ENDPOINT (CRUD directo) ======
response = requests.post(
    f"{BASE_URL}/api/contents",
    json={
        "platform": "Facebook",
        "title": "Mi post",
        "tone": "informal",
        "content": "Contenido del post",
        "hashtags": "#facebook",
        "link": "https://link.com"
    }
)
print("Post creado:", response.json())
```

---

## ✨ Resumen de Endpoints

**POST /api/contents/generate - ARQUITECTURA ACTUALIZADA:**
- ✅ Solo requiere `prompt`
- ✅ La plataforma se especifica **dentro del prompt**
- ✅ El LLM identifica automáticamente la plataforma desde el texto del prompt
- ✅ Si no especificas plataforma en el prompt, usa "X" como defecto
- ✅ Genera automáticamente: platform (detectada), title, tone, content, hashtags

**Ventaja:** API simplificada y más natural. El usuario solo necesita describir lo que quiere de forma natural.

---

# Aclaraciones sobre Swagger/OpenAPI

## Pregunta: ¿Por qué Swagger muestra `platform: "X"` en el endpoint `/api/contents/generate`?

### Respuesta:

En Swagger, aunque un campo sea **OPCIONAL**, el interfaz OpenAPI lo sigue mostrando en el ejemplo JSON para referencia.

---

## ✅ LO QUE DEBES SABER:

### Campo `platform` EN `/api/contents/generate`:

**Status:** ⭐ **COMPLETAMENTE OPCIONAL**

```json
// ✅ CORRECTO - Solo prompt (recomendado y más simple)
{
  "prompt": "Crea un post motivacional"
}

// ✅ TAMBIÉN CORRECTO - Con platform especificada
{
  "prompt": "Crea un post motivacional",
  "platform": "LinkedIn"
}

// ✅ TAMBIÉN CORRECTO - Platform "X" explícito (pero innecesario)
{
  "prompt": "Crea un post motivacional",
  "platform": "X"
}
```

---

## 🔍 Cómo verificar en Swagger:

1. Accede a `http://localhost:8000/docs`
2. Busca el endpoint `POST /api/contents/generate`
3. En la descripción verás:
   ```
   IMPORTANTE: Solo se requiere el campo `prompt`. 
   El campo `platform` es completamente opcional (usa "X" por defecto si no se especifica).
   ```

4. En el modelo `GeneratePostRequest` verás:
   - `prompt` (requerido) ✅
   - `platform` (opcional) ⭐

---

## 📝 Diferencia entre endpoints:

### POST `/api/contents` (CRUD directo):
- `platform` → **REQUERIDO** ✅
- `title` → **REQUERIDO** ✅
- `tone` → **REQUERIDO** ✅
- `content` → **REQUERIDO** ✅

### POST `/api/contents/generate` (IA):
- `prompt` → **REQUERIDO** ✅
- `platform` → **OPCIONAL** ⭐ (default: "X")

---

## 💡 Conclusión:

**En Swagger, `platform` aparece en el proyecto, pero:**
- ✅ NO es requerido
- ✅ Si no lo envías, se usa "X" automáticamente
- ✅ La documentación del endpoint lo aclara explícitamente

**Usa solo lo que necesites:**
```bash
# Mínimo requerido
curl -X POST "http://localhost:8000/api/contents/generate" \
  -d '{"prompt": "Tu descripción aquí"}'
```

---

# Estructura del Proyecto

```
Actividad/
├── m3_omar_pinzon.py              # Aplicación principal FastAPI
├── test_m3_omar_pinzon.py         # Tests unitarios con pytest
├── requirements.txt               # Dependencias del proyecto
├── settingsApp.json               # Configuración de la app y BD
├── settingsLLM.json               # Configuración de Azure OpenAI
├── README.md                      # Documentación completa
├── run.bat                        # Script para ejecutar en Windows
├── run.sh                         # Script para ejecutar en Linux/Mac
├── agents.md                      # Especificaciones del rol y proyecto
├── .venv/                         # Entorno virtual
├── .git/                          # Control de versiones
└── __pycache__/                   # Cache de Python
```

### Descripción de archivos principales:

- **m3_omar_pinzon.py**: Aplicación FastAPI con todos los endpoints, modelos y lógica de negocio
- **test_m3_omar_pinzon.py**: Tests unitarios con pytest para validar la funcionalidad
- **requirements.txt**: Listado de dependencias externas necesarias
- **settingsApp.json**: Configuración de conexión a base de datos y API
- **settingsLLM.json**: Configuración de Azure OpenAI y parámetros del modelo
- **run.bat / run.sh**: Scripts para ejecutar fácilmente la aplicación
- **.venv**: Entorno virtual de Python con todas las dependencias instaladas

---

# Tecnologías Utilizadas

### Backend
- **FastAPI** (0.109.0): Framework web moderno y rápido para construcción de APIs REST
- **Uvicorn** (0.27.0): Servidor ASGI para ejecutar la aplicación FastAPI

### Base de Datos
- **SQLAlchemy** (2.0.24): ORM para mapeo objeto-relacional con MySQL
- **mysql-connector-python** (8.2.0): Conector MySQL para Python

### IA y LLMs
- **openai** (1.6.1): Cliente Python para Azure OpenAI APIs

### Validación de Datos
- **Pydantic** (2.5.2): Validación de datos con type hints
- **pydantic-settings** (2.1.0): Gestión de configuración con Pydantic

### Desarrollo y Testing
- **pytest** (7.4.3): Framework para tests unitarios
- **pytest-asyncio** (0.21.1): Plugin para testing de código asincrónico
- **httpx** (0.25.2): Cliente HTTP para testing
- **python-dotenv** (1.0.0): Carga de variables de entorno

---

# Solución de Problemas

### Error: "Can't connect to MySQL server"
- ✅ Verifica que MySQL Server está en ejecución
- ✅ Verifica usuario/contraseña en `settingsApp.json`
- ✅ Verifica que la base de datos `social_media_db` existe
- ✅ Comprueba el puerto MySQL (por defecto 3306)
- ✅ Intenta conectar manualmente: `mysql -u root -p social_media_db`

### Error: "Can't connect to OpenAI"
- ✅ Verifica las credenciales en `settingsLLM.json`
- ✅ Verifica que tienes acceso a Azure OpenAI
- ✅ Verifica que no hay firewall bloqueando la conexión
- ✅ Valida que el endpoint de Azure es correcto
- ✅ Comprueba que el deployment_name existe en Azure

### Error: "Port 8000 already in use"
- ✅ Cambia el puerto en el archivo `m3_omar_pinzon.py` (última línea)
- ✅ O detén la aplicación anterior que usa ese puerto
- ✅ Usa: `netstat -ano | findstr :8000` (Windows) para identificar el proceso

### Error: "Module not found"
- ✅ Verifica que el entorno virtual está activado
- ✅ Ejecuta: `pip install -r requirements.txt`
- ✅ Verifica que los archivos de configuración existen en el directorio raíz

### Error: "JSON parse error" al generar contenido
- ✅ Verifica que Azure OpenAI está respondiendo
- ✅ Intenta con un prompt más simple primero
- ✅ Aumenta el valor de `max_tokens` en `settingsLLM.json`

### La tabla no se crea automáticamente
- ✅ Verifica que la base de datos `social_media_db` existe
- ✅ Verifica permisos de usuario MySQL
- ✅ Ejecuta manualmente: `CREATE TABLE social_media_posts...` (ver arriba)
- ✅ Revisa los logs de la aplicación para más detalles

---

## Notas de Desarrollo

- El proyecto está tipado completamente para mayor seguridad
- La configuración se carga desde archivos JSON externos
- La API incluye manejo de errores y validaciones con Pydantic v2
- Se puede extender fácilmente con nuevos campos en los esquemas Pydantic
- La generación de enlaces fake es automática si el LLM no proporciona uno real
- Los posts se identifican automáticamente por el LLM desde el prompt
- El proyecto sigue convenciones de camelCase para nombres de variables y funciones

---

## Licencia

Uso académico - Actividad 3 - Programa Avanzado de IA para Programar

Maestría en Inteligencia Artificial - Módulo 3

Autor: Omar Pinzón

---

## Contacto y Soporte

Para reportar problemas o sugerencias, consulta la documentación de Swagger en: `http://localhost:8000/docs`
