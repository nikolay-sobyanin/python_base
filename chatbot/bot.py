# -*- coding: utf-8 -*-
import logging
import random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

try:
    from local_config import GROUP_ID, TOKEN
except ImportError:
    exit('Do cp local_config.py.default local_config.py and set token')

# TO DO: сделайте отдельный файл local_config.py
#  В него вынесите id группы и токен. Сам файл добавьте в гит.игнор.

#  осталось local_config.py удалить. Вы его сначала запушили, а потом добавили в гитигнор.
#  Т.е. он сейчас индексируется. Если я сделаю изменения, они отобразятся у вас.
#  .
#  И еще из local_config.py.default удалите настоящие данные.
#  А токен вообще теперь нужно регенировать. Токены никогда не палим. Иначе ваш бот начнет слать просьбы сделать
#  перевод на чью-нибудь карту.

log = logging.getLogger('bot')


def config_logging():
    log.setLevel(logging.DEBUG)

    strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(fmt=strfmt, datefmt=datefmt))
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename='bot.log', encoding="utf8")
    file_handler.setFormatter(logging.Formatter(fmt=strfmt, datefmt=datefmt))
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
        self.vk = vk_api.VkApi(token=self.token, api_version='5.130')
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        """Run bot"""
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except:
                log.exception('Ошибка в обработке события.')

    def on_event(self, event):
        """
        Send massage back if it's text
        :param event: VkBotMessageEvent object
        :return: None
        """

        if event.type == VkBotEventType.MESSAGE_NEW:
            self.api.messages.send(
                message=event.message.text,
                random_id=random.randint(0, 2 ** 20),
                peer_id=event.message.peer_id
            )
            log.debug('Отправили сообщение назад.')
        else:
            log.info(f'Мы пока не умеем обрабатывать события тип {event.type}')


def main():
    config_logging()
    bot = Bot(GROUP_ID, TOKEN)
    bot.run()


if __name__ == '__main__':
    main()
