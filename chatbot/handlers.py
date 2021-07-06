import re

re_city = re.compile(r'^[\w\-\s]{3,30}$')
re_date = re.compile(r'^\d{2}-\d{2}-\d{4}$')
re_email = re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b')


def handle_city_from(text, context):
    match = re.match(re_city, text)
    if match:
        context['city_from'] = text
        return True
    else:
        return False


def handle_city_to(text, context):
    match = re.match(re_city, text)
    if match:
        context['city_to'] = text
        return True
    else:
        return False


def handle_date(text, context):
    match = re.match(re_date, text)
    if match:
        context['date'] = text
        return True
    else:
        return False


def handle_email(text, context):
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context['email'] = matches[0]
        return True
    else:
        return False
