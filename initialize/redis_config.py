import redis
import logging

redis_client = None

def initialize_redis_cache():
    global redis_client
    try:
        redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        if redis_client.ping():
            logging.info("Redis cache initialized successfully")
        else:
            raise Exception("Redis ping failed")
    except Exception as e:
        logging.error(f"Failed to initialize Redis cache: {e}")
