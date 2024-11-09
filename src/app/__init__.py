from fastapi import FastAPI

from .routes import router

apps_config = {
    "debug": True,
    "title": "IQA Web Service",
    "version": "0.1.0",
    "docs_url": "/",
    "swagger_ui_parameters": {
        "displayRequestDuration": True,
        "defaultModelsExpandDepth": 0,
        "filter": True,
    },
}

app: FastAPI = FastAPI(**apps_config)

app.router.include_router(router)
