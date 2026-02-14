# Se desarrollará una aplicación en Python que implemente una API REST backend con FastAPI capaz de generar contenido estructurado para redes sociales por medio de prompts y almacenarlo en base de datos. El contenido

La API debe tenr:
- Conexión a base de datos MySQL y los settings de conexion se deben leerse y cargarse de un archivo de configuracion llamado 'settingsApp.json'.
- los esquemas relacionados con base de datos deben ser con Pydantic para manejar todo en formato json.
- Generación de modelo SQLAlchemy:
Pydantic con campos:
* id (primary key).
* platform (X, LinkedIn, Facebook, etc).
* title (título o tema del artículo).
* tone (estilo: formal, informal, divertido).
* content (campo texto largo).
* hashtags (hashtags sugeridos).
* link (enlace a recurso externo).
* created_at (fecha creación se crea automática a nivel de base de datos).
* Agregar más campos si se quiere.

-	Generación de Schemas con Pydantic:
* SocialMediaPostSchema.
* SocialMediaPostSchemas.

- Generación de endpoints para el API REST:
* GET /api/contents devuelve todos los SocialMediaPost.
* GET /api/ contents/{id} devuelve un SocialMediaPost por su ID.
* POST /api/contents permite enviar un objeto json con un nuevo SocialMediaPost que se almacene en base de datos directamente.
* POST /api/contents/generate permite enviar un objeto json con un campo prompt que se usará en backend para generar un nuevo SocialMediaPost. Este contenido debe ser generado por un LLM gestionado por el backend donde se configure de tal forma que las respuestas sean en formato json usando Pydantic para ser gestionadas como SocialMediaPost.
* PUT /api/contents/{id} permite enviar un objeto json con un SocialMediaPost que ya existe y se modifique algún campo y se almacene en base de datos directamente.
* DELETE /api/contents/{id} permite borrar un SocialMediaPost por su ID.


# Integracion del LLM:

* El proyecto debe usar la libreria OpenAI para la conexion con LLMs de azure.
* EL proyecto debe poder personalizar las interacciones del LLM ajustando los parámetros de comportamiento (temperature, max_tokens, top_p, etc.). Estos parametros edbe estar en un archivo de configuraciion llamado 'settingsLLM.json' el cual debe ser leido y cargado para ser usado en las interaccion con el modelo de lenguaje.
* el archivo 'settingsLLM.json'contendrá adicionalmente los settings necesarios para crear una conexión con OpenAI, en este archivo debe estar el endpoint, deployment_name y api_key.

# Documentación del proyecto

Generar un README que incluya:

-   Objetivo del proyecto.
-   Instrucciones de instalación y ejecución.
-   Ejemplo de uso.
