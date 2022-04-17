from dependency_injector import containers, providers

from app.services.bot.vfs_tracking_bot import VfsTrackingBot
from app.services.machines.categories_machine.category_checking_machine import CategoryCheckingMachine
from app.services.machines.dates_machine.date_checking_machine import DateCheckingMachine
from app.services.machines.machine_factory import MachineFactory
from app.services.machines.site_machine.site_checking_machine import SiteCheckingMachine
from app.services.machines.state_factory import StateFactory
from app.services.security import Security
from app.services.tracker import Tracker


class Services(containers.DeclarativeContainer):

    config = providers.Configuration()
    repos = providers.DependenciesContainer()

    state_factory = providers.Singleton(
        StateFactory,
        login_repo=repos.login,
        center_repo=repos.center,
        category_repo=repos.category,
        post_repo=repos.post,
        action_repo=repos.action
    )

    machine_factory = providers.Singleton(
        MachineFactory,
        state_factory=state_factory,
        action_repo=repos.action
    )
    # ==================================
    category_machine = providers.Factory(
        CategoryCheckingMachine,
        factory=state_factory,
        action_repo=repos.action
    )

    date_machine = providers.Factory(
        DateCheckingMachine,
        factory=state_factory,
        action_repo=repos.action
    )

    site_machine = providers.Factory(
        SiteCheckingMachine,
        action_repo=repos.action
    )
    # ==================================
    __security = providers.Singleton(
        Security,
        bot_login=config.BOT_LOGIN,
        bot_password=config.BOT_PASSWORD,
        account_repo=repos.account,
        cheat_repo=repos.cheat
    )

    __tracker = providers.Singleton(
        Tracker,
        factory=machine_factory,
        login_repo=repos.login,
        post_repo=repos.post
    )

    bot = providers.Singleton(
        VfsTrackingBot,
        token=config.TOKEN,
        chat_actor_id=config.CHAT_ID,
        security=__security,
        tracker=__tracker,
        dev_chat_id=config.DEV_CHAT_ID,
        logins_encoded=config.LOGINS_ENCODED
    )
