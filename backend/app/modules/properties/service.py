from app.modules.properties.repository import PropertyRepository
from app.modules.properties.schemas import PropertyCreate, PropertyUpdate

class PropertyService:
    
    def __init__(self, db):
        self.property_repo = PropertyRepository(db)

    def get_property(self, property_id: str | None = None):
        
        return self.property_repo.get_property(property_id)

    def create_property(self, property_in: PropertyCreate):
        
        #criar e chamar função de gerar slug automatico
        if not property_in.slug:
            property_in.slug = "batata52"    
        
        status = self.property_status_check(property_in)
        property_data = property_in.model_dump()
        
        property_data["status"] = status
        
        return self.property_repo.create_property(property_data)

    def property_status_check(self, property_data: dict):
        
        important_fields = [
            "owner_id"
            "property_type",
            "transaction_type",
            "area",
            "address",
            "district",
            "city",
            "state",
            "zip_code"
        ]
        
        if property_data.property_type:
            if property_data.property_type == "APT":
                important_fields.extend([
                    "iptu",
                    "iptu_type",
                    "condominium_fee",
                    "bedrooms",
                    "bathrooms",
                    "garage_spots"
                ])
            elif property_data.property_type == "CAS":
                important_fields.extend([
                    "iptu",
                    "iptu_type",
                    "bedrooms",
                    "bathrooms",
                    "garage_spots"
                ])
        
        if property_data.transaction_type:
            if property_data.transaction_type == "rent":
                important_fields.append("price_rent")
            elif property_data.transaction_type == "sale": 
                important_fields.append("price_sale")
        
         
        for field in important_fields:
            value = getattr(property_data, field, None)
            
            if value is None or value == "" or value == 0:
                return "register incomplete"
        
        print(important_fields)
        return "registed"
    
    def update_property(self, property_in: PropertyUpdate):
        
        property = self.property_repo.get_property(property_in.id)
        
        #validar se slug foi mudado, caso tenha sido validar se é unico e em caso de erro voltar HHTP_RESPONSE
        
        status = self.property_status_check(property_in)
        property_data = property_in.model_dump()
        
        property_data["status"] = status
        
        return self.property_repo.update_property(property_data)
        