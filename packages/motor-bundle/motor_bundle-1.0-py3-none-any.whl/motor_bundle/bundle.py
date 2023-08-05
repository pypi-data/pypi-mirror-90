from applauncher.event import ConfigurationReadyEvent
from dependency_injector import providers

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, validator

class MotorConfig(BaseModel):
    uri: str

    @validator('uri')
    def uri_validator(cls, v):
        if not v.startswith('mongodb://'):
            raise ValueError('Uri should starts with mongodb://')
        return v


class MotorBundle:
    def __init__(self):
        self.config_mapping = {
            "motor": MotorConfig
        }

        self.event_listeners = [
            (ConfigurationReadyEvent, self.configuration_ready),
        ]

        self.injection_bindings = {}

    def configuration_ready(self, event):
        config = event.configuration.motor

        self.injection_bindings[AsyncIOMotorClient] = providers.Singleton(
            AsyncIOMotorClient,
            config.uri
        )
