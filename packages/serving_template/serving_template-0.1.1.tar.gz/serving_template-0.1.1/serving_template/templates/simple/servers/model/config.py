import os


def get_env(variable_name, default=None, func=lambda x: x):
    return func(os.environ.get(variable_name, default))


class AppConfig(object):
    # model setting
    MODEL_PATH = get_env('MODEL_PATH', './model')
    BATCH_SIZE = get_env('INFERENCE_BATCH_SIZE', 64, int)
    MODEL_SLEEP = get_env('MODEL_SLEEP', 0.1, float)

    # redis setting
    REDIS_BROKER = get_env('REDIS_BROKER', 'localhost:6379', lambda x: x if ':' in x else f'{x}:6379')
    REDIS_QUEUE = get_env('REDIS_QUEUE', 'REDIS_QUEUE')
