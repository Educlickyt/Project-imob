from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import app.modules.models

app = FastAPI()

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.roles.router import router as roles_router
from app.modules.properties.router import router as properties_router, media_router
from app.modules.propertyOwners.router import router as propertyOwners_router
from app.modules.leads.router import router as leads_router
from app.modules.clients.router import router as clients_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.apiKeys.router import router as apikeys_router
from app.modules.domains.router import router as domains_router
from app.api.public.router import router as public_router


class CustomCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Pega headers relevantes
        origin = request.headers.get("origin", "")
        api_key = request.headers.get("x-api-key", "")
        
        # Processa a requisição
        response = await call_next(request)
        
        # Se tem API Key → permite qualquer origem
        if api_key:
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "X-API-Key, Content-Type, Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        # Se é do frontend local → permite localhost (ERP)
        elif origin in ["http://localhost:5173"]:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Headers"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "*"
        
        return response

app.add_middleware(CustomCORSMiddleware)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(properties_router)
app.include_router(media_router)
app.include_router(propertyOwners_router)
app.include_router(leads_router)
app.include_router(clients_router)
app.include_router(dashboard_router)
app.include_router(apikeys_router)
app.include_router(domains_router)
app.include_router(public_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Atris Imob API",
        version="1.0.0",
        description="API interna do Atris imob",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "description": "JWT token de autenticação. Obtenha via /auth/login ou /auth/register"
        }
    }
    
    # Aplicar segurança apenas às rotas que precisam de autenticação
    protected_paths = ["/users/","/roles", "/properties", "/auth/logout", "/propertyOwners", "/leads", "/clients", "/dashboard", "/api-keys", "/domains"]
    
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]:
                # Verificar se a rota precisa de autenticação
                if any(path.startswith(protected) for protected in protected_paths):
                    openapi_schema["paths"][path][method]["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def root():
    return {"message": "FastAPI funcionando!"}

