from app.modules.properties.models import Property

class PropertyRepository:
    
    def __init__(self, db):
       self.db = db 
    
    def create_property(self, property_data: dict):
        
        db_property = Property(**property_data)
        self.db.add(db_property)
        self.db.commit()
        self.db.refresh(db_property)
        
        return db_property
    
    def get_property(self, property_id: str | None = None):
        
        if property_id:
            return self.db.query(Property).filter(Property.id == property_id).first()
        
        return self.db.query(Property).all()
        
    def update_property(self, property_data: dict):
        
        db_property = Property(**property_data)
        