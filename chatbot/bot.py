# -*- coding: utf-8 -*-
import logging

from _token import token

import random
import vk_api
from vk_api import bot_longpoll

group_id = 203294647

log = logging.getLogger('bot')
stream_handler = logging.StreamHandler()
log.addHandler(stream_handler)
log.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.DEBUG)

class Bot:

    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token

        self.vk = vk_api.VkApi(token=self.token)
        self.long_poller = bot_longpoll.VkBotLongPoll(self.vk, self.group_id)

        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка в обработке события.')
                # print(exc)

    def on_event(self, event):
        if event.type == bot_longpoll.VkBotEventType.MESSAGE_NEW:
            self.api.messages.send(
                message=event.object.message['text'],
                random_id=random.randint(0, 2 ** 20),
                peer_id=event.object.message['peer_id']
            )
            log.info('Отправили сообщение назад.')
            # print('Ты сказал:', event.object.message['text'])
        else:
            log.debug(f'Мы пока не умеем обрабатывать события тип {event.type}')
            # print(f'Мы пока не умеем обрабатывать события тип {event.type}')


def main():
    bot = Bot(group_id, token)
    bot.run()


if __name__ == '__main__':
    main()
