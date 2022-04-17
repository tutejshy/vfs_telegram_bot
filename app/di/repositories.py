from dependency_injector import containers, providers

from app.repo.account_repo import AccountRepo
from app.repo.action_repo import ActionRepo
from app.repo.category_repo import CategoryRepo
from app.repo.center_repo import CenterRepo
from app.repo.cheat_repo import CheatRepo
from app.repo.login_repo import LoginRepo
from app.repo.post_repo import PostRepo


class Repositories(containers.DeclarativeContainer):

    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    account = providers.Singleton(
        AccountRepo,
        engine=gateways.database_engine
    )

    login = providers.Singleton(
        LoginRepo,
        engine=gateways.database_engine
    )

    cheat = providers.Singleton(
        CheatRepo,
        engine=gateways.database_engine
    )

    action = providers.Singleton(
        ActionRepo,
        engine=gateways.database_engine
    )

    center = providers.Singleton(
        CenterRepo,
        engine=gateways.database_engine
    )

    category = providers.Singleton(
        CategoryRepo,
        engine=gateways.database_engine
    )

    post = providers.Singleton(
        PostRepo,
        engine=gateways.database_engine
    )
