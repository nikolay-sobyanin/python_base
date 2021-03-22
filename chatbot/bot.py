# -*- coding: utf-8 -*-
import logging
import random
import vk_api
from vk_api import bot_longpoll

try:
    from local_config import GROUP_ID, TOKEN
except ImportError:
    exit('Do cp local_config.py.default local_config.py and set token')


# TODO: сделайте отдельный файл local_config.py
#  В него вынесите id группы и токен. Сам файл добавьте в гит.игнор.

log = logging.getLogger('bot')
log.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename='bot.log', encoding="utf8")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
file_handler.setLevel(logging.DEBUG)

log.addHandler(stream_handler)
log.addHandler(file_handler)


class Bot:
    """
    Echo bot for vk.com
    Use Python 3.8
    """
    def __init__(self, group_id, token):
        """
        :param group_id: group id from vk.com
        :param token:  secret token
        """
        self.group_id = group_id
        self.token = token

        # TODO: переключитесь на API версии 5.120, не меньше.
        #  У VkApi есть параметр api_version, который по умолчанию стоит на 5.92 (это старая динозавр-версия)
        #  Не забудьте в группе поменять версию API.
        #  Так же учтите, что event в run изменится. Текст сообщения начнет хранится в другом поле!
        # Я в самом начале переключил на версию 5.130. Я изменил уже путь к тексту сообщения.
        self.vk = vk_api.VkApi(token=self.token)
        self.long_poller = bot_longpoll.VkBotLongPoll(self.vk, self.group_id)

        self.api = self.vk.get_api()

    def run(self):
        """Run bot"""
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка в обработке события.')

    def on_event(self, event):
        """
        Send massage back if it's text
        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type == bot_longpoll.VkBotEventType.MESSAGE_NEW:
            self.api.messages.send(
                message=event.object.message['text'],
                random_id=random.randint(0, 2 ** 20),
                peer_id=event.object.message['peer_id']
            )
            log.debug('Отправили сообщение назад.')
        else:
            log.debug(f'Мы пока не умеем обрабатывать события тип {event.type}')


def main():
    bot = Bot(GROUP_ID, TOKEN)
    bot.run()


if __name__ == '__main__':
    main()
