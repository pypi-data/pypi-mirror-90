#!/usr/bin/env bash

if [[ $# < 1 ]]; then
    echo 'usage: ./build_image.sh version'
    exit 1
fi

# build web server docker for process request
WEB_SERVER_NAME=yourname/proj-web-server:$1
WEB_RUN_CMD='gunicorn -c servers/web/gunicorn_config.py servers.web.main:app'

docker build -f ./Dockerfile --build-arg RUN_CMD="$WEB_RUN_CMD" -t $WEB_SERVER_NAME .. || exit
docker push $WEB_SERVER_NAME || exit

# build model server docker for process 
MODEL_SERVER_NAME=yourname/proj-model-server:$1
MODEL_RUN_CMD='env PYTHONPATH=. python -m servers.model.main'

docker build -f ./Dockerfile --build-arg RUN_CMD="$MODEL_RUN_CMD" -t $MODEL_SERVER_NAME .. || exit
docker push $MODEL_SERVER_NAME || exit