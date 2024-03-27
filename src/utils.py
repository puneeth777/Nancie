from datetime import datetime

from src.config import Config


def get_base_format():
    return {'message_queue': []}


def get_system_prompt(user_name):
    return [{"role": "system", "content": Config().get_system_prompt()},
            {"role": "user", "content": f'Hi {Config().get_bot_name()}, my name is {user_name}'},
            {"role": "assistant", "content": f'Hi {user_name}! Nice to meet you. Feel free to ask me anything you '
                                             f'want to know, and I\'ll be more than happy to help you. Go on, '
                                             f'ask away! What\'s on your mind?'}]


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
