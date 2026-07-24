from fastapi import HTTPException, status
from app.modules.clients.repository import ClientRepository
from datetime import datetime, timezone

class ClientService:
    
    def __init__(self, db):
        self.client_repo = ClientRepository(db)
    
    def create(self, current_user, client_in: dict):
        # validar existencia de email no banco se existir campo email em client_in
        # validar existencia de telefone no banco se existir campo phone em client_in
        
        client_data = client_in.model_dump()
        client_data['tenant_id'] = current_user.tenant_id
        
        return self.client_repo.create(client_data)
    
    def list(self, current_user):
        db_clients = self.client_repo.get_clients(current_user.tenant_id)
        
        if not db_clients:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clients not found."
            )
        
        return db_clients
    
    def get(self, current_user, client_id: str):
        db_client = self.client_repo.get_by_id(client_id, current_user.tenant_id)
        
        if not db_client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found."
            )
        return db_client
    
    def update(self, current_user, client_id: str, client_in: dict):
        db_client = self.client_repo.get_by_id(client_id, current_user.tenant_id)
        
        if not db_client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found."
            )
        
        update_data = client_in.model_dump(exclude_unset=True)
        
        if not update_data:
            return db_client
        
        return self.client_repo.update(db_client, update_data)
    
    def delete(self, current_user, client_id: str):
        db_client = self.client_repo.get_by_id(client_id, current_user.tenant_id)
        
        if not db_client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found."
            )
        
        self.client_repo.update(db_client, {"deleted_at": datetime.now(timezone.utc)})
        return