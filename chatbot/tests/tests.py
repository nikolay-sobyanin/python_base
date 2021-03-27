from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from vk_api.bot_longpoll import VkBotMessageEvent

from bot import Bot


class TestWorkBot(TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {'message': {'date': 1616865208, 'from_id': 11965090, 'id': 113, 'out': 0, 'peer_id': 11965090,
                               'text': 'Hello', 'conversation_message_id': 113, 'fwd_messages': [],
                               'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False},
                   'client_info': {
                       'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'callback',
                                          'intent_subscribe', 'intent_unsubscribe'],
                       'keyboard': True,
                       'inline_keyboard': True,
                       'carousel': False, 'lang_id': 0}
                   },
        'group_id': 203294647,
        'event_id': 'ba3f4b7fc833693601702d4186ff771bac8af840'
    }

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.run()
                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                self.assertEqual(bot.on_event.call_count, count)

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)
        send_mock = Mock()
        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll'):
                bot = Bot('', '')
                bot.api = Mock()
                bot.api.messages.send = send_mock
                bot.on_event(event)

        send_mock.assert_called_once_with(
            message=self.RAW_EVENT['object']['message']['text'],
            random_id=ANY,
            peer_id=self.RAW_EVENT['object']['message']['peer_id']
        )
