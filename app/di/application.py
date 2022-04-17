from dependency_injector import containers, providers

from app.core.settings import Settings
from app.di.core import Core
from app.di.gateways import Gateways
from app.di.repositories import Repositories
from app.di.services import Services


class Application(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Settings()])

    core = providers.Container(
        Core,
        config=config,
    )

    gateways = providers.Container(
        Gateways,
        config=config,
    )

    repos = providers.Container(
        Repositories,
        config=config,
        gateways=gateways,
    )

    services = providers.Container(
        Services,
        config=config,
        repos=repos,
    )
