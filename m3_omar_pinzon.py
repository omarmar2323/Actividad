"""
Social Media Content Generator API
Aplicación FastAPI para generar contenido estructurado para redes sociales usando LLMs de Azure.
"""

import json
import os
import uuid
import re
from typing import Optional, List
from datetime import datetime
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String, DateTime, Integer, func, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from openai import OpenAI


# ======================
# Configuración
# ======================

def loadConfigFile(filePath: str) -> dict:
    """Carga un archivo de configuración JSON."""
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {filePath}")
    with open(filePath, 'r', encoding='utf-8') as file:
        return json.load(file)


appConfig: dict = loadConfigFile("settingsApp.json")
llmConfig: dict = loadConfigFile("settingsLLM.json")

# Configuración de base de datos
dbConfig = appConfig.get("database", {})
dbConnectionString: str = (
    f"mysql+mysqlconnector://{dbConfig.get('user')}:{dbConfig.get('password')}"
    f"@{dbConfig.get('host')}:{dbConfig.get('port', 3306)}/{dbConfig.get('database')}"
)

# ======================
# Modelos SQLAlchemy
# ======================

Base = declarative_base()



class SocialMediaPostModel(Base):
    """Modelo de base de datos para posts de redes sociales."""
    __tablename__ = "social_media_posts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    tone = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    hashtags = Column(Text, nullable=True)
    link = Column(String(500), nullable=False)  # SIEMPRE requerido
    createdAt = Column(DateTime, default=datetime.utcnow, server_default=func.now())


# ======================
# Esquemas Pydantic
# ======================

class SocialMediaPostSchema(BaseModel):
    """Schema para un post de red social."""
    platform: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=255)
    tone: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1)
    hashtags: Optional[str] = None
    link: str = Field(..., min_length=1, description="Enlace siempre generado por el LLM (real o fake)")

    class Config:
        from_attributes = True


class SocialMediaPostSchemas(BaseModel):
    """Schema para respuesta de posts con ID."""
    id: int
    platform: str
    title: str
    tone: str
    content: str
    hashtags: Optional[str] = None
    link: str
    createdAt: datetime

    class Config:
        from_attributes = True


class GeneratePostRequest(BaseModel):
    """Schema para solicitud de generación de contenido.
    
    Solo requiere el prompt. La plataforma se especifica dentro del prompt.
    Por defecto es 'X' si no se especifica en el prompt.
    """
    prompt: str = Field(
        ..., 
        min_length=10, 
        description="Descripción del contenido a generar. Puede incluir la plataforma destino",
        json_schema_extra={"example": "Crea un post motivacional sobre programación para LinkedIn"}
    )


# ======================
# Inicialización de la aplicación
# ======================

app = FastAPI(
    title=appConfig["api"]["title"],
    version=appConfig["api"]["version"],
    description=appConfig["api"]["description"]
)

# Engine y sesión de base de datos
engine = None
SessionLocal = None

def initializeDatabase() -> None:
    """Inicializa la conexión a la base de datos."""
    global engine, SessionLocal
    if engine is None:
        engine = create_engine(dbConnectionString, echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # Crear tablas si no existen
        Base.metadata.create_all(bind=engine)

# Inicializar base de datos al arrancar la aplicación
@app.on_event("startup")
async def startupEvent():
    """Event que se ejecuta al iniciar la aplicación."""
    initializeDatabase()

# Cliente de OpenAI (compatible con Azure y Ollama local)
llmEndpoint: str = llmConfig["openai"]["endpoint"]
llmApiKey: str = llmConfig["openai"]["api_key"]

# Si el endpoint contiene 'localhost' u 'openai.azure.com', usar el cliente apropiado
if "localhost" in llmEndpoint or "192.168" in llmEndpoint or "127.0.0.1" in llmEndpoint:
    # Ollama local o similar - usar OpenAI con base_url
    openaiClient = OpenAI(
        api_key=llmApiKey,
        base_url=llmEndpoint
    )
else:
    # Azure OpenAI - usar base_url para compatibilidad
    openaiClient = OpenAI(
        api_key=llmApiKey,
        base_url=llmEndpoint
    )


# ======================
# Funciones auxiliares
# ======================

def generateFakeLink(title: str) -> str:
    """Genera un enlace fake basado en el título del post.
    
    Args:
        title: Título del post
    
    Returns:
        URL fake con formato https://resources.example.com/{slug}
    """
    # Convertir el título a slug (minúsculas, sin espacios/caracteres especiales)
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    # Limitar a 50 caracteres
    slug = slug[:50]
    # Generar URL fake
    uniqueId = str(uuid.uuid4())[:8]
    return f"https://resources.example.com/{slug}-{uniqueId}"


@contextmanager
def getDbSession():
    """Context manager para manejo de sesiones de base de datos."""
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call initializeDatabase() first.")
    dbSession: Session = SessionLocal()
    try:
        yield dbSession
        dbSession.commit()
    except Exception as e:
        dbSession.rollback()
        raise e
    finally:
        dbSession.close()


def generateSocialMediaContent(prompt: str) -> tuple:
    """
    Genera contenido para redes sociales usando Azure OpenAI.
    El LLM identifica la plataforma del prompt. Si no la especifica, usa "X" por defecto.
    
    Args:
        prompt: Descripción del contenido a generar (puede incluir la plataforma destino)
    
    Returns:
        tuple: (SocialMediaPostSchema generado, plataforma identificada)
    """
    modelParams = llmConfig.get("model_parameters", {})
    
    systemPrompt = """Eres un experto en generación de contenido para redes sociales.
Analizarás el prompt para identificar la plataforma de red social destino (X, LinkedIn, Facebook, Instagram, TikTok, etc.).
Si la plataforma NO está especificada claramente, usa "X" como plataforma por defecto.

Responde SIEMPRE en formato JSON válido con esta estructura exacta:
{
    "platform": "plataforma identificada (X, LinkedIn, Facebook, etc.)",
    "title": "título o tema del artículo",
    "tone": "estilo (formal, informal, divertido)",
    "content": "contenido del post",
    "hashtags": "hashtags separados por espacios",
    "link": "enlace a recurso externo (REQUERIDO - genera uno relevante al contenido si no tienes uno real)"
}
No incluyas markdown ni caracteres especiales en el JSON.
Importante: Siempre incluye el campo "platform" en la respuesta.
IMPRESCINDIBLE: El campo "link" NUNCA debe estar vacío o null. Si no conoces un link real, genera uno fake basado en el tema del post (ej: https://blog.example.com/tema-del-post)."""

    try:
        response = openaiClient.chat.completions.create(
            model=llmConfig["openai"]["deployment_name"],
            messages=[
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": prompt}
            ],
            temperature=modelParams.get("temperature", 0.7),
            max_tokens=modelParams.get("max_tokens", 1500),
            top_p=modelParams.get("top_p", 0.95),
            frequency_penalty=modelParams.get("frequency_penalty", 0.0),
            presence_penalty=modelParams.get("presence_penalty", 0.0)
        )
    except Exception as connError:
        raise ConnectionError(
            f"Error de conexión con el LLM. Endpoint: {llmEndpoint} | Modelo: {llmConfig['openai']['deployment_name']} | "
            f"Detalles: {str(connError)}"
        )
    
    # Extraer el contenido de la respuesta
    responseContent: str = response.choices[0].message.content
    
    # Parsear JSON de la respuesta
    try:
        # Intentar encontrar JSON válido en la respuesta
        jsonStart = responseContent.find('{')
        jsonEnd = responseContent.rfind('}') + 1
        if jsonStart >= 0 and jsonEnd > jsonStart:
            jsonStr = responseContent[jsonStart:jsonEnd]
            generatedData: dict = json.loads(jsonStr)
        else:
            generatedData: dict = json.loads(responseContent)
    except json.JSONDecodeError:
        generatedData: dict = {
            "platform": "X",
            "title": "Error en generación",
            "tone": "neutral",
            "content": responseContent,
            "hashtags": "",
            "link": generateFakeLink("Error en generación")
        }
    
    # Extraer la plataforma del JSON generado
    detectedPlatform: str = generatedData.get("platform", "X")
    if not detectedPlatform or detectedPlatform.strip() == "":
        detectedPlatform = "X"
    
    # Extraer y validar el link (NUNCA debe estar vacío)
    generatedTitle: str = generatedData.get("title", "Sin título")
    generatedLink: str = generatedData.get("link", "")
    
    # Si el link está vacío o es None, generar uno fake
    if not generatedLink or generatedLink.strip() == "":
        generatedLink = generateFakeLink(generatedTitle)
    
    return (
        SocialMediaPostSchema(
            platform=detectedPlatform,
            title=generatedTitle,
            tone=generatedData.get("tone", "neutral"),
            content=generatedData.get("content", ""),
            hashtags=generatedData.get("hashtags", ""),
            link=generatedLink
        ),
        detectedPlatform
    )


# ======================
# Endpoints de la API REST
# ======================

@app.get("/", tags=["Health"])
async def root() -> dict:
    """Endpoint raíz para verificar que la API está funcionando."""
    return {
        "message": "Social Media Content Generator API",
        "version": appConfig["api"]["version"],
        "status": "running"
    }


@app.get("/api/contents", response_model=List[SocialMediaPostSchemas], tags=["Posts"])
async def getAllContents() -> List[SocialMediaPostSchemas]:
    """Obtiene todos los posts de redes sociales."""
    with getDbSession() as dbSession:
        posts = dbSession.query(SocialMediaPostModel).all()
        return [SocialMediaPostSchemas.from_orm(post) for post in posts]


@app.get("/api/contents/{postId}", response_model=SocialMediaPostSchemas, tags=["Posts"])
async def getContentById(postId: int) -> SocialMediaPostSchemas:
    """Obtiene un post específico por su ID."""
    with getDbSession() as dbSession:
        post = dbSession.query(SocialMediaPostModel).filter(
            SocialMediaPostModel.id == postId
        ).first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post con ID {postId} no encontrado"
            )
        
        return SocialMediaPostSchemas.from_orm(post)


@app.post("/api/contents", response_model=SocialMediaPostSchemas, tags=["Posts"])
async def createContent(postData: SocialMediaPostSchema) -> SocialMediaPostSchemas:
    """Crea un nuevo post directamente."""
    with getDbSession() as dbSession:
        newPost = SocialMediaPostModel(
            platform=postData.platform,
            title=postData.title,
            tone=postData.tone,
            content=postData.content,
            hashtags=postData.hashtags,
            link=postData.link
        )
        dbSession.add(newPost)
        dbSession.flush()
        
        return SocialMediaPostSchemas.from_orm(newPost)


@app.post("/api/contents/generate", response_model=SocialMediaPostSchemas, tags=["Posts"])
async def generateContent(request: GeneratePostRequest) -> SocialMediaPostSchemas:
    """
    Genera un nuevo post usando un LLM basado en un prompt.
    
    El LLM identificará la plataforma del prompt.
    Si la plataforma no está especificada en el prompt, usa "X" por defecto.
    
    Ejemplos:
    - Con plataforma explícita: "Crea un post sobre IA para LinkedIn"
    - Sin plataforma (por defecto X): "Crea un post sobre IA"
    """
    try:
        # Generar contenido usando el LLM (el LLM identifica la plataforma)
        generatedPost, _ = generateSocialMediaContent(request.prompt)
        
        # Guardar en base de datos
        with getDbSession() as dbSession:
            newPost = SocialMediaPostModel(
                platform=generatedPost.platform,
                title=generatedPost.title,
                tone=generatedPost.tone,
                content=generatedPost.content,
                hashtags=generatedPost.hashtags,
                link=generatedPost.link
            )
            dbSession.add(newPost)
            dbSession.flush()
            
            return SocialMediaPostSchemas.from_orm(newPost)
    
    except ConnectionError as connErr:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"LLM no disponible: {str(connErr)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar contenido: {str(e)}"
        )


@app.put("/api/contents/{postId}", response_model=SocialMediaPostSchemas, tags=["Posts"])
async def updateContent(postId: int, postData: SocialMediaPostSchema) -> SocialMediaPostSchemas:
    """Actualiza un post existente."""
    with getDbSession() as dbSession:
        post = dbSession.query(SocialMediaPostModel).filter(
            SocialMediaPostModel.id == postId
        ).first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post con ID {postId} no encontrado"
            )
        
        post.platform = postData.platform
        post.title = postData.title
        post.tone = postData.tone
        post.content = postData.content
        post.hashtags = postData.hashtags
        post.link = postData.link
        
        dbSession.flush()
        return SocialMediaPostSchemas.from_orm(post)


@app.delete("/api/contents/{postId}", tags=["Posts"])
async def deleteContent(postId: int) -> dict:
    """Elimina un post por su ID."""
    with getDbSession() as dbSession:
        post = dbSession.query(SocialMediaPostModel).filter(
            SocialMediaPostModel.id == postId
        ).first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post con ID {postId} no encontrado"
            )
        
        dbSession.delete(post)
        
        return {"message": f"Post con ID {postId} eliminado exitosamente"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "m3_omar_pinzon:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
