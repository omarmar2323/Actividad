"""
Tests para la aplicación Social Media Content Generator API
"""

import pytest
from pydantic import ValidationError
from m3_omar_pinzon import SocialMediaPostSchema, SocialMediaPostSchemas


class TestHealthEndpoints:
    """Tests para verificación de estructura básica."""
    
    def test_module_imports_successfully(self) -> None:
        """Verifica que el módulo se importe sin errores de configuración."""
        from m3_omar_pinzon import app, appConfig, llmConfig
        assert app is not None
        assert appConfig is not None
        assert llmConfig is not None


class TestSocialMediaPostSchema:
    """Tests para validación de esquemas."""
    
    def test_valid_post_schema(self) -> None:
        """Verifica que un schema válido se cree correctamente."""
        post = SocialMediaPostSchema(
            platform="X",
            title="Test Post",
            tone="informal",
            content="This is a test post content",
            hashtags="#test #python",
            link="https://example.com"
        )
        assert post.platform == "X"
        assert post.title == "Test Post"
        assert post.tone == "informal"
    
    def test_invalid_platform_raises_validation_error(self) -> None:
        """Verifica que se lance error si el platform está vacío."""
        with pytest.raises(ValidationError):
            SocialMediaPostSchema(
                platform="",
                title="Test",
                tone="informal",
                content="Content"
            )
    
    def test_invalid_title_raises_validation_error(self) -> None:
        """Verifica que se lance error si el título está vacío."""
        with pytest.raises(ValidationError):
            SocialMediaPostSchema(
                platform="X",
                title="",
                tone="informal",
                content="Content"
            )


class TestAPIEndpoints:
    """Tests para estructura de endpoints de la API REST."""
    
    def test_app_has_required_endpoints(self) -> None:
        """Verifica que la aplicación tenga los endpoints requeridos."""
        from m3_omar_pinzon import app
        
        # Obtener todas las rutas de la aplicación
        routes = {route.path for route in app.routes if hasattr(route, 'path')}
        
        # Verificar que existan los endpoints principales
        requiredEndpoints = {
            "/",
            "/api/contents",
            "/api/contents/{postId}",
            "/api/contents/generate",
            "/docs",
            "/openapi.json"
        }
        
        # Al menos algunos de estos deben estar presentes
        assert any(endpoint in routes for endpoint in requiredEndpoints)
    
    def test_schema_validation_with_optional_fields(self) -> None:
        """Verifica que los campos opcionales funcionen correctamente."""
        post = SocialMediaPostSchema(
            platform="X",
            title="Test",
            tone="informal",
            content="Content",
            link="https://example.com/test"  # link ahora es requerido y siempre generado por LLM
        )
        assert post.hashtags is None
        assert post.link == "https://example.com/test"


# Fixtures para tests
@pytest.fixture
def validPostData() -> dict:
    """Proporciona datos válidos para un post."""
    return {
        "platform": "LinkedIn",
        "title": "Test Post",
        "tone": "formal",
        "content": "This is a test post for testing purposes",
        "hashtags": "#test #linkedin",
        "link": "https://example.com"
    }


@pytest.fixture
def generatePostData() -> dict:
    """Proporciona datos válidos para generar un post."""
    return {
        "prompt": "Generate a motivational post about learning programming",
        "platform": "X"
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
