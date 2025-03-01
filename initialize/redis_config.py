import redis
import logging
import os

redis_client = None

def initialize_redis_cache():
    global redis_client
    try:
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
        if redis_client.ping():
            logging.info("Redis cache initialized successfully")
        else:
            raise Exception("Redis ping failed")
    except Exception as e:
        logging.error(f"Failed to initialize Redis cache: {e}")
