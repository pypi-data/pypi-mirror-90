import os


def get_env(variable_name, default=None, func=lambda x: x):
    return func(os.environ.get(variable_name, default))


class AppConfig(object):
    SERVER_LISTEN = get_env('SERVER_LISTEN', '0.0.0.0:15527')
    WEB_WORKER_NUM = get_env('WEB_WORKER_NUM', 8, int)
    WEB_MAX_TRIES = get_env('WEB_MAX_TRIES', 6000, int)
    WEB_SLEEP = get_env('WEB_SLEEP', 0.1, float)

    # redis setting
    REDIS_BROKER = get_env('REDIS_BROKER', 'localhost:6379', lambda x: x if ':' in x else f'{x}:6379')
    REDIS_QUEUE = get_env('REDIS_QUEUE', 'REDIS_QUEUE')
