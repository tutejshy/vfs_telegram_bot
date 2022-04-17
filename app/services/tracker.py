import datetime
from typing import List, Callable, Optional, Union

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING, STATE_STOPPED
from pytz import utc

from app.core.build_config import BuildConfig
from app.models.domain.post_db import PostStatus
from app.models.schema.login_schema import LoginMerge
from app.repo.login_repo import LoginRepo

from app.repo.post_repo import PostRepo
from app.services.machines.machine_factory import MachineFactory, Machine
from app.util.util import make_message_from_posts


class Tracker:
    def __init__(self, factory: MachineFactory, login_repo: LoginRepo, post_repo: PostRepo):
        self._scheduler = BackgroundScheduler(job_defaults={'max_instances': 4}, timezone=utc)
        self._factory = factory
        self._login_repo = login_repo
        self._post_repo = post_repo
        self._messanger: Optional[Callable] = None

    def setup(self):
        self._scheduler.remove_all_jobs()

        if BuildConfig.DEBUG:
            self._scheduler.add_job(self._check, 'interval', minutes=1)
        else:
            count = self._login_repo.get_number_of_logins()
            if count > 0:
                update_time_in_minutes = 60 / count
                if update_time_in_minutes == 0:
                    update_time_in_minutes = 1
                elif update_time_in_minutes > 10:
                    update_time_in_minutes = 10

                self._scheduler.add_job(self._check, 'interval', minutes=update_time_in_minutes)

    def start(self):
        self.stop()
        if self._login_repo.has_logins():
            self.setup()
            self._scheduler.start()

    def stop(self):
        if self._scheduler.state != STATE_STOPPED:
            self._scheduler.shutdown()

    def _check(self):
        print("_begin check")
        try:
            site_checking_machine = self._factory.of(Machine.SITE)
            if site_checking_machine and site_checking_machine.exec():
                category_checking_machine = self._factory.of(Machine.DICTIONARY)
                if category_checking_machine and category_checking_machine.exec():
                    date_checking_machine = self._factory.of(Machine.DATES)
                    if date_checking_machine and date_checking_machine.exec():
                        self.__check_posts()
        except Exception as err:
            print(err)
        print("_end check")

    def set_messanger_callback(self, fun: Optional[Callable]):
        self._messanger = fun

    def register_logins(self, items: List[LoginMerge]) -> bool:
        registered = self._login_repo.register_logins(items)
        restart = self._scheduler.state == STATE_RUNNING
        if restart and registered:
            self.start()

        return registered

    def __check_posts(self):
        routes = self._login_repo.get_available_routes()
        for item in routes:
            posts = self._post_repo.get_latest_posts_by(item.route)
            if posts:
                self._messanger(make_message_from_posts(posts))
                for post in posts:
                    post.status = PostStatus.POSTED
                    post.updated_at = datetime.datetime.now()
                self._post_repo.merge_all(posts)

    def clear(self):
        self.stop()
        self._login_repo.clear()
