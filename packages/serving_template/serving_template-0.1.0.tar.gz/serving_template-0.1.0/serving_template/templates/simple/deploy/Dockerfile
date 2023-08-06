FROM docker-registry.yimian.com.cn/pytorch-1.4-cuda10.0:v1

# setting for locale, to avoid UnicodeDecodeError
ENV LC_ALL=C.UTF-8
COPY ./requirements.txt /env/requirements.txt

RUN pip install --no-cache-dir -r /env/requirements.txt


ADD . /app
WORKDIR /app

# setting for model server
ENV MODEL_PATH = get_env('MODEL_PATH', './model')
ENV BATCH_SIZE 64
ENV MODEL_SLEEP 0.1


# setting for web server
ENV SERVER_LISTEN '0.0.0.0:15527'
ENV WEB_WORKER_NUM 8
ENV WEB_MAX_TRIES 6000
ENV WEB_SLEEP 0.1

# setting for redis broker
ENV REDIS_BROKER 'localhost:6379'
ENV REDIS_QUEUE 'REDIS_QUEUE'


ARG RUN_CMD
ENV RUN_CMD ${RUN_CMD:-'gunicorn -c servers/web/gunicorn_config.py servers.web.main:app'}
CMD $RUN_CMD