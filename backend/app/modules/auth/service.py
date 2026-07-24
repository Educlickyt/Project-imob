from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.modules.users.repository import UserRepository
from app.modules.roles.repository import RoleRepository
from app.modules.tenants.repository import TenantRepository
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import RegisterRequest, UserResponse, TenantResponse
from app.core.security import create_access_token, verify_password, create_refresh_token_string
from datetime import timedelta, timezone, datetime


class AuthService:
     
    def __init__(self, db):
        self.user_repo = UserRepository(db)
        self.tenant_repo = TenantRepository(db)
        self.role_repo = RoleRepository(db)
        self.auth_repo = AuthRepository(db)
 
    def register_tenant(self, user_in: RegisterRequest):
        user_exists = self.user_repo.get_by_email(user_in.email)
         
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esse email já está cadastrado."
            )
          
        tenant_slug = user_in.tenant_slug
        if not tenant_slug:
            tenant_slug = self._generate_slug(user_in.tenant_name)
            
        tenant_exists = self.tenant_repo.get_by_slug(tenant_slug)
        if tenant_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este slug de tenant já está em uso."
            )
        
        tenant_data = {
            "name": user_in.tenant_name,
            "slug": tenant_slug,
            "plan": "free",
            "status": "active"
        }
        db_tenant = self.tenant_repo.create(tenant_data)
        
        user_data = user_in.model_dump()
        user_data.pop('tenant_name', None)
        user_data.pop('tenant_slug', None)
        user_data['tenant_id'] = db_tenant.id
        
        
        db_user = self.user_repo.create(user_data)
        
        admin_role = self.role_repo.get_admin_role()
                
        self.user_repo.link_user_to_role(db_user.id, admin_role.id)
        
        permissions = self.user_repo.get_user_permissions_keys(db_user.id)
                
        
        access_token = create_access_token(
            data={
                    "sub": str(db_user.id),
                    "tenant_id": str(db_tenant.id),
                    "roles": [admin_role.name],
                    "permissions": permissions
                  }
        )
        
        token_str = create_refresh_token_string()
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        self.auth_repo.save_refresh_token(db_user.id, token_str, expires_at)

        response = JSONResponse(content=jsonable_encoder({
            "user": UserResponse.model_validate(db_user),
            "tenant": TenantResponse.model_validate(db_tenant),
            "access_token": access_token,
            "token_type": "bearer"
        }))
        
        response.set_cookie(
            key="refresh_token",
            value=token_str,
            httponly=True,   
            secure=True,       
            samesite="lax",   
            expires=expires_at
        )
        
        return response
    
    def _generate_slug(self, name: str) -> str:
        import re
        slug = name.lower()
        slug = re.sub(r'[áàâãäå]', 'a', slug)
        slug = re.sub(r'[éèêë]', 'e', slug)
        slug = re.sub(r'[íìîï]', 'i', slug)
        slug = re.sub(r'[óòôõö]', 'o', slug)
        slug = re.sub(r'[úùûü]', 'u', slug)
        slug = re.sub(r'[ç]', 'c', slug)
        slug = re.sub(r'[ñ]', 'n', slug)
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')
        return slug
        
    def authenticate_user(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Seu acesso foi bloqueado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        tenant = self.tenant_repo.get_by_id(user.tenant_id)
        if tenant.status != 'active':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Essa conta está suspensa",
                headers={"WWW-Authenticate": "Bearer"},
            )
       
        roles = self.user_repo.get_user_roles(user.id)
        permissions = self.user_repo.get_user_permissions_keys(user.id)
        
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "tenant_id": str(user.tenant_id),
                "roles": roles,
                "permissions": permissions
            }
        )
        
        token_str = create_refresh_token_string()
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        self.auth_repo.save_refresh_token(user.id, token_str, expires_at)

        response = JSONResponse(content={
            "access_token": access_token,
            "token_type": "bearer"
        })
        
        response.set_cookie(
            key="refresh_token",
            value=token_str,
            httponly=True,   
            secure=True,       
            samesite="lax",   
            expires=expires_at
        )
        
        
        return response
        
    def refresh_access_token(self, token_str: str):
        
        if not token_str:
            raise HTTPException(status_code=401, detail="Refresh token ausente.")

        
        db_token = self.auth_repo.get_refresh_token(token_str)
                
        if not db_token or db_token.is_expired:
            response = JSONResponse(
                status_code=401,
                content={"detail": "Refresh token inválido ou expirado."}
            )
            response.delete_cookie(key="refresh_token")
            return response

        user = self.user_repo.get_by_id(db_token.user_id) 
        
        if not user:
            response = JSONResponse(
                status_code=401,
                content={"detail": "Sua conta foi desativada."}
            ) 
            response.delete_cookie(key="refresh_token")
            return response
        
        if not user.is_active:
            response = JSONResponse(
                status_code=401,
                content={"detail": "Sua conta foi suspensa."}
            ) 
            response.delete_cookie(key="refresh_token")
            return response

        roles = self.user_repo.get_user_roles(user.id)
        permissions = self.user_repo.get_user_permissions_keys(user.id)

        new_access_token = create_access_token(data={
            "sub": str(user.id),
            "tenant_id": str(user.tenant_id),
            "roles": roles,
            "permissions": permissions
        })
        
        response = JSONResponse(content={
            "access_token": new_access_token,
            "token_type": "bearer"
        })

        new_refresh_token = create_refresh_token_string()
        refresh_token_exp = datetime.now(timezone.utc) + timedelta(days=7)
        
        self.auth_repo.rotate_refresh_token(db_token, new_refresh_token, refresh_token_exp)
        
        response.set_cookie(
            key="refresh_token",
            value= new_refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            expires= refresh_token_exp
        )
        
        return response
    
    def logout_user(self, token_str):
        
        refresh_token = self.auth_repo.get_refresh_token(token_str)
        
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possível encontrar o refresh token"
            )
        
        self.auth_repo.delete_refresh_token(refresh_token)
        
        response = JSONResponse(
                status_code=204,
                content={}
            )
        response.delete_cookie(key="refresh_token")
        
        return response
    
    def logout_all_user(self, token_str):
        
        refresh_token = self.auth_repo.get_refresh_token(token_str)
        
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possível encontrar o refresh token"
            )
        
        self.auth_repo.delete_all_user_tokens(refresh_token.user_id)
        
        response = JSONResponse(
                status_code=200,
                content={"detail": "Todos os dispositivos foram deslogados"}
            )
        
        response.delete_cookie(key="refresh_token")
        
        return response