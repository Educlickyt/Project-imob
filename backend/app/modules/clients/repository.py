from app.modules.clients.models import Client

class ClientRepository:
    
    def __init__(self, db):
        self.db = db
        
    def create(self, client_data: dict):
        db_client = Client(**client_data)
        self.db.add(db_client)
        self.db.commit()
        self.db.refresh(db_client)
        return db_client
        
    def get_clients(self, tenant_id):
        return self.db.query(Client).filter(Client.tenant_id == tenant_id, Client.deleted_at.is_(None)).all()
        
    def get_by_id(self, client_id, tenant_id):
        return self.db.query(Client).filter(Client.id == client_id, Client.tenant_id == tenant_id, Client.deleted_at.is_(None)).first()
    
    def update(self, db_client: Client, update_data: dict):
        for key, value in update_data.items():
            setattr(db_client, key, value)
        self.db.commit()
        self.db.refresh(db_client)
        return db_client
        