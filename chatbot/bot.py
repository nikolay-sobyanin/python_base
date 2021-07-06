# -*- coding: utf-8 -*-
import logging
import random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import settings
import handlers

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


class UserState:
    """Состояние пользователя внутри сценрия"""

    def __init__(self, scenario_name, step_name, context=None):
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.context = context or {}


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
        self.user_states = dict()  # user_id -> UserState

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

        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info(f'Мы пока не умеем обрабатывать события тип {event.type}')
            return

        user_id = event.message.peer_id
        text = event.message.text

        if user_id in self.user_states:
            # continue scenario
            text_to_send = self.continue_scenario(user_id, text=text)
        else:
            # search intent
            for intent in settings.INTENTS:
                if any(token in text.lower() for token in intent['tokens']):
                    # run intent
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self.start_scenario(intent['scenario'], user_id)
                    break
            else:
                text_to_send = settings.DEFAULT_ANSWER

        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id
        )

    def start_scenario(self, scenario_name, user_id):
        scenario = settings.SCENARIO[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self.user_states[user_id] = UserState(scenario_name=scenario_name, step_name=first_step)
        return text_to_send

    def continue_scenario(self, user_id, text):
        state = self.user_states[user_id]
        steps = settings.SCENARIO[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        if handler(text=text, context=state.context):
            # next step
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                # switch to next step
                state.step_name = step['next_step']
            else:
                # finish scenario
                self.user_states.pop(user_id)
        else:
            # retry current step
            text_to_send = step['failure_text'].format(**state.context)

        return text_to_send


def main():
    config_logging()
    bot = Bot(GROUP_ID, TOKEN)
    bot.run()


if __name__ == '__main__':
    main()
