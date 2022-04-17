from app.db.session import DBEngine

from dependency_injector import containers, providers


class Gateways(containers.DeclarativeContainer):

    config = providers.Configuration()

    database_engine = providers.Singleton(
        DBEngine,
        database_uri=config.DATABASE_URI
    )
