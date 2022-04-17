from app.di.application import Application
from app.services.bot.vfs_tracking_bot import VfsTrackingBot


def startup():
    application = Application()
    application.core.init_resources()
    application.wire(modules=[__name__])
    application.core.build()

    bot: VfsTrackingBot = application.services.bot()

    bot.idle()


if __name__ == "__main__":
    startup()
