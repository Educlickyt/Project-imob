from fastapi import HTTPException, status
from app.modules.users.repository import UserRepository
from app.modules.roles.repository import RoleRepository
from app.modules.tenants.repository import TenantRepository
from app.modules.auth.schemas import RegisterRequest, UserResponse, TenantResponse
from app.core.security import create_access_token, verify_password
from datetime import timedelta

class AuthService:
     
    def __init__(self, db):
        self.user_repo = UserRepository(db)
        self.tenant_repo = TenantRepository(db)
        self.role_repo = RoleRepository(db)
 
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
        
        return {
            "user": UserResponse.model_validate(db_user),
            "tenant": TenantResponse.model_validate(db_tenant),
            "access_token": access_token,
            "token_type": "bearer"
        }
    
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
                detail="Seu acesso foi bloqueada",
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
        
        return {"access_token": access_token, "token_type": "bearer"}
        