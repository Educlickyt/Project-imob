from fastapi import HTTPException

from app.modules.showcaseConfigs.repository import ShowcaseConfigRepository
from app.modules.showcaseConfigs.schemas import ShowcaseConfigUpdate


class ShowcaseConfigService:
    def __init__(self, db):
        self.repo = ShowcaseConfigRepository(db)

    def get_config(self, tenant_id):
        config = self.repo.get_by_tenant(tenant_id)

        if not config:
            config = self.repo.create({
                "tenant_id": tenant_id,
                "template": "classic",
                "is_active": True,
            })

        return config

    def update_config(self, tenant_id, config_in: ShowcaseConfigUpdate):
        config = self.repo.get_by_tenant(tenant_id)

        if not config:
            raise HTTPException(status_code=404, detail="Showcase config not found")

        update_data = config_in.model_dump(exclude_unset=True)

        if not update_data:
            return config

        if "template" in update_data:
            valid_templates = ["classic", "list", "featured"]
            if update_data["template"] not in valid_templates:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid template. Must be one of: {valid_templates}"
                )

        return self.repo.update(config, update_data)

    def get_config_for_public(self, tenant_id):
        config = self.get_config(tenant_id)
        return {
            "template": config.template,
            "primary_color": config.primary_color,
            "secondary_color": config.secondary_color,
        }
