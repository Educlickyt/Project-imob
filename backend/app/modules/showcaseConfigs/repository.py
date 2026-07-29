from app.modules.showcaseConfigs.models import ShowcaseConfig


class ShowcaseConfigRepository:
    def __init__(self, db):
        self.db = db

    def get_by_tenant(self, tenant_id) -> ShowcaseConfig | None:
        return (
            self.db.query(ShowcaseConfig)
            .filter(ShowcaseConfig.tenant_id == tenant_id)
            .first()
        )

    def create(self, config_data: dict) -> ShowcaseConfig:
        db_config = ShowcaseConfig(**config_data)
        self.db.add(db_config)
        self.db.commit()
        self.db.refresh(db_config)
        return db_config

    def update(self, db_config: ShowcaseConfig, update_data: dict) -> ShowcaseConfig:
        for key, value in update_data.items():
            setattr(db_config, key, value)
        self.db.commit()
        self.db.refresh(db_config)
        return db_config
