import html
import json
import traceback
from typing import Dict, Optional

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

from app.services.security import Security
from app.services.tracker import Tracker

from app.util.util import read_csv, read_encoded_csv


class VfsTrackingBot:
    def __init__(self, token: str, chat_actor_id: str, security: Security, tracker: Tracker,
                 dev_chat_id: Optional[str] = None,
                 logins_encoded: Optional[str] = None):
        self._chat_actor_id = chat_actor_id
        self._dev_chat_id = dev_chat_id
        self._updater = Updater(token)
        self._tracker = tracker
        self._security = security
        self._logins_encoded = logins_encoded

    def _tracker_handler(self, text: str):
        job = self._updater.job_queue
        job.run_once(self._tracker_message, 2, context={"message": text})

    def _tracker_message(self, context: CallbackContext):
        if isinstance(context.job.context, Dict):
            message = context.job.context["message"]
            context.bot.send_message(chat_id=self._chat_actor_id, text=message, parse_mode=ParseMode.HTML)

    def _clear(self, update: Update, context: CallbackContext):
        if self._security.logged_in(update.effective_chat.id):
            print("clear")

    def _documents(self, update: Update, context: CallbackContext):
        if update.message.document.mime_type == 'text/comma-separated-values':
            if self._security.logged_in(update.effective_chat.id):
                file_id = update.message.document.file_id
                file_name = update.message.document.file_name

                tmp_path = context.bot.getFile(file_id).download(file_name)
                self._tracker.register_logins(read_csv(tmp_path))

    def _start(self, update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot!")

    def _login(self, update: Update, context: CallbackContext):
        actor_id = update.effective_chat.id
        flag = self._security.login(actor_id, context.args)
        text = "success" if flag else "failure"
        context.bot.send_message(chat_id=actor_id, text=text)

    def _start_tracking(self, update: Update, context: CallbackContext):
        if self._security.logged_in(update.effective_chat.id):
            self._tracker.start()

    def _stop_tracking(self, update: Update, context: CallbackContext):
        if self._security.logged_in(update.effective_chat.id):
            self._tracker.stop()

    def _error_handler(self, update: object, context: CallbackContext) -> None:
        if self._dev_chat_id:
            tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)

            update_str = update.to_dict() if isinstance(update, Update) else str(update)
            message = (
                f'An exception was raised while handling an update\n'
                f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
                '</pre>\n\n'
                f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
                f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
                f'<pre>{html.escape("".join(tb_list))}</pre>'
            )
            # message 4096 characters limit
            context.bot.send_message(chat_id=self._dev_chat_id, text=message, parse_mode=ParseMode.HTML)

    def _setup(self):

        dispatcher = self._updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', self._start))
        dispatcher.add_handler(CommandHandler('login', self._login))
        dispatcher.add_handler(CommandHandler('start_tracking', self._start_tracking))
        dispatcher.add_handler(CommandHandler('stop_tracking', self._stop_tracking))
        dispatcher.add_handler(MessageHandler(Filters.document, self._documents))
        dispatcher.add_error_handler(self._error_handler)

        self._tracker.set_messanger_callback(self._tracker_handler)

        logins = read_encoded_csv(self._logins_encoded or "")
        self._tracker.register_logins(logins)
        self._tracker.start()

        self._updater.start_polling()

    def idle(self):
        self._setup()
        self._updater.idle()
