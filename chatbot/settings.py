
HELP = '/help'
TICKET = '/ticket'

info = f'Для начала заказа билетов введите команду {TICKET}'

INTENTS = [
    {
        'name': 'Справка',
        'tokens': (HELP, 'справка', 'информ'),
        'scenario': None,
        'answer': info,
    },
    {
        'name': 'Заказ билетов',
        'tokens': TICKET,
        'scenario': 'booking',
        'answer': None,
    },
]

SCENARIO = {
    'booking': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Введите город отправления.',
                'failure_text': 'Название города должно состоять из 3-30 букв и дефиса. Попробуйте еще раз...',
                'handler': 'handle_city_from',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введите город прибытия.',
                'failure_text': 'Название города должно состоять из 3-30 букв и дефиса. Попробуйте еще раз...',
                'handler': 'handle_city_to',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Введите дату отправления.',
                'failure_text': 'Введите дату в формате DD-MM-YYYY',
                'handler': 'handle_date',
                'next_step': 'step4'
            },
            'step4': {
                'text': 'Введите email',
                'failure_text': 'Введите email.',
                'handler': 'handle_email',
                'next_step': 'step5'
            },
            'step5': {
                'text': 'Спасибо за регистрацию! Мы отправили на {email} информацию о рейсах'
                        '\nиз {city_from} в {city_to} на дату {date}',
                'failure_text': None,
                'handler': None,
                'next_step': None
            },

        }
    }
}

DEFAULT_ANSWER = info
