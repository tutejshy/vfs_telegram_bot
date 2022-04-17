from dependency_injector import containers, providers

from app.core.build_config import BuildConfig


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()

    class BuildConfigurator:
        def __init__(self, debug: bool = False):
            BuildConfig.DEBUG = debug

    build = providers.Singleton(
        BuildConfigurator,
        debug=config.DEBUG,
    )
