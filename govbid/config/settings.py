"""Application configuration for the GovBid engine.

Settings are loaded from environment variables prefixed with ``GOVBID_``
using pydantic-settings. These settings define which policy pack is
used by default. In a future SaaS deployment, these may be loaded
from a database or secrets manager instead.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GOVBID_", extra="ignore")

    # Default policy pack to load when generating new dossiers. This can be
    # overridden per-request in the API layer.
    default_policy_pack: str = "govbid_default"


settings = Settings()
