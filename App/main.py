from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers import progress, user, session

app = FastAPI(
    title="ZenSpace API",
    description="API sécurisée avec authentification JWT (OAuth2)",
    version="1.0.0"
)

app.include_router(user.router)
app.include_router(session.router)
app.include_router(progress.router)

@app.get("/")
def root():
    return {"message": "ZenSpace API works 🚀"}

# ✅ Swagger compatible avec OAuth2PasswordBearer
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/users/login",
                    "scopes": {}
                }
            }
        }
    }

    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
