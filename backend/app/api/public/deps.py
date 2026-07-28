from fastapi import Request, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.tenants.repository import TenantRepository
from app.modules.domains.repository import DomainRepository


def get_tenant_from_request(request: Request, slug: str = None) -> dict:
    """
    Resolve qual tenant está sendo acessado.
    
    Dois caminhos:
    1. Slug na URL → busca tenant pelo slug
    2. Domínio próprio → busca tenant pelo Host header
    """
    # Abre sessão do banco
    db: Session = next(get_db())
    
    try:
        # CAMINHO 1: Slug fornecido na URL
        # Ex: /v1/joao-silva/properties → slug = "joao-silva"
        if slug:
            tenant_repo = TenantRepository(db)
            tenant = tenant_repo.get_by_slug(slug)
            
            if not tenant:
                raise HTTPException(
                    status_code=404,
                    detail="Tenant not found"
                )
                
            if not tenant.is_public:
                raise HTTPException(
                    status_code=404,
                    detail="Tenant not found"
                )
            
            return {"tenant_id": tenant.id, "slug": tenant.slug}
        
        # CAMINHO 2: Domínio próprio (Host header)
        # Ex: Host: www.joaosilva.com.br → busca em tenant_domains
        host = request.headers.get("host", "")
        
        # Remove porta se existir (ex: "localhost:8000" → "localhost")
        host = host.split(":")[0]
        
        # Ignora domínios do próprio sistema
        # (para não resolver imobapp.com como um tenant)
        system_domains = ["localhost", "imobapp.com", "127.0.0.1"]
        if host in system_domains:
            raise HTTPException(
                status_code=404,
                detail="Use slug format for system domains"
            )
        
        # Busca o domínio no banco
        domain_repo = DomainRepository(db)
        db_domain = domain_repo.get_by_domain(host)
        
        if not db_domain:
            raise HTTPException(
                status_code=404,
                detail="Domain not configured"
            )
        
        # Busca o tenant pelo ID do domínio
        tenant_repo = TenantRepository(db)
        tenant = tenant_repo.get_by_id(db_domain.tenant_id)
        
        if not tenant:
            raise HTTPException(
                status_code=404,
                detail="Tenant not found"
            )
        
        if not tenant.is_public:
            raise HTTPException(
                status_code=404,
                detail="Tenant not found"
            )
        
        return {"tenant_id": tenant.id, "slug": tenant.slug}
    
    finally:
        db.close()