from gevent import monkey

monkey.patch_all()

from servers.web.config import AppConfig

bind = AppConfig.SERVER_LISTEN
workers = AppConfig.WEB_WORKER_NUM
worker_class = 'gevent'
timerout = 60
log_level = AppConfig.LOG_LEVEL
preload_app = True
