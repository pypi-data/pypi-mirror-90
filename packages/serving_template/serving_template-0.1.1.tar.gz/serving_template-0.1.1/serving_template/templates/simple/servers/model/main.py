from serving_agent import ModelAgent

from servers.model.config import AppConfig
from servers.model.ModelClass import ModelClass

if __name__ == "__main__":
    model_agent = ModelAgent(
        redis_broker=AppConfig.REDIS_BROKER,
        redis_queue=AppConfig.REDIS_QUEUE,
        model_class=ModelClass,
        batch_size=AppConfig.BATCH_SIZE,
        model_sleep=AppConfig.MODEL_SLEEP,
    )
    model_agent.run()
