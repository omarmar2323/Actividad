"""
Social Media Content Generator API
Aplicación FastAPI para generar contenido estructurado para redes sociales usando LLMs de Azure.
"""

import json
import os
from typing import Optional, List
from datetime import datetime
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String, DateTime, Integer, func, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from openai import AzureOpenAI


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
    link = Column(String(500), nullable=True)
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
    link: Optional[str] = None

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
    link: Optional[str] = None
    createdAt: datetime

    class Config:
        from_attributes = True


class GeneratePostRequest(BaseModel):
    """Schema para solicitud de generación de contenido."""
    prompt: str = Field(..., min_length=10)
    platform: str = Field(default="X", min_length=1, max_length=50)


# ======================
# Inicialización de la aplicación
# ======================

app = FastAPI(
    title=appConfig["api"]["title"],
    version=appConfig["api"]["version"],
    description=appConfig["api"]["description"]
)

# Engine y sesión de base de datos
engine = create_engine(dbConnectionString, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Cliente de Azure OpenAI
azureOpenAIClient = AzureOpenAI(
    api_key=llmConfig["openai"]["api_key"],
    api_version=llmConfig["openai"]["api_version"],
    azure_endpoint=llmConfig["openai"]["endpoint"]
)


# ======================
# Funciones auxiliares
# ======================

@contextmanager
def getDbSession():
    """Context manager para manejo de sesiones de base de datos."""
    dbSession: Session = SessionLocal()
    try:
        yield dbSession
        dbSession.commit()
    except Exception as e:
        dbSession.rollback()
        raise e
    finally:
        dbSession.close()


def generateSocialMediaContent(prompt: str, platform: str) -> SocialMediaPostSchema:
    """
    Genera contenido para redes sociales usando Azure OpenAI.
    
    Args:
        prompt: Descripción del contenido a generar
        platform: Plataforma de red social (X, LinkedIn, Facebook, etc.)
    
    Returns:
        SocialMediaPostSchema: Post generado con estructura JSON
    """
    modelParams = llmConfig.get("model_parameters", {})
    
    systemPrompt = f"""Eres un experto en generación de contenido para redes sociales. 
Debes generar contenido estructurado para la plataforma {platform}.
Responde SIEMPRE en formato JSON válido con esta estructura exacta:
{{
    "title": "título o tema del artículo",
    "tone": "estilo (formal, informal, divertido)",
    "content": "contenido del post",
    "hashtags": "hashtags separados por espacios",
    "link": "enlace a recurso externo (opcional)"
}}
No incluyas markdown ni caracteres especiales en el JSON."""

    response = azureOpenAIClient.chat.completions.create(
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
            "title": "Error en generación",
            "tone": "neutral",
            "content": responseContent,
            "hashtags": "",
            "link": None
        }
    
    return SocialMediaPostSchema(
        platform=platform,
        title=generatedData.get("title", "Sin título"),
        tone=generatedData.get("tone", "neutral"),
        content=generatedData.get("content", ""),
        hashtags=generatedData.get("hashtags", ""),
        link=generatedData.get("link")
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
    """Genera un nuevo post usando un LLM basado en un prompt."""
    try:
        # Generar contenido usando Azure OpenAI
        generatedPost = generateSocialMediaContent(request.prompt, request.platform)
        
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
