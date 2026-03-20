import redis

def get_redis_connection():
    # Conexión local a Redis, db=1 como se solicitó
    return redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
