from fam.settings.update import Update


class Settings:

    @property
    def update(self):
        return self._update

    def __init__(self) -> None:
        self._update: Update = Update()


settings: Settings = Settings()
