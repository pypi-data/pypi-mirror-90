from serving_agent import WebAgent
from flask import Flask, jsonify, request

from servers.web.config import AppConfig

app = Flask(__name__)
web_agent = WebAgent(
    redis_broker=AppConfig.REDIS_BROKER, redis_queue=AppConfig.REDIS_QUEUE, web_sleep=AppConfig.WEB_SLEEP, max_tries=AppConfig.WEB_MAX_TRIES
)


@app.route('/api/test', methods=['POST'])
def test():
    parmas = request.get_json()
    data = parmas['data']
    result = web_agent.process(data)
    return jsonify({'data': result})


if __name__ == '__main__':
    app.run(debug=True)
