import redis
from app.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)

class RedisService:
    @staticmethod
    def set_refresh_token(user_id: str, refresh_token: str, expire_days: int = 7):
        redis_client.setex(f"refresh_token:{user_id}", expire_days * 24 * 60 * 60, refresh_token)
    
    @staticmethod
    def get_refresh_token(user_id: str) -> str:
        return redis_client.get(f"refresh_token:{user_id}")
    
    @staticmethod
    def delete_refresh_token(user_id: str):
        redis_client.delete(f"refresh_token:{user_id}")
    
    @staticmethod
    def blacklist_token(token: str, expire_seconds: int):
        redis_client.setex(f"blacklist:{token}", expire_seconds, "true")
    
    @staticmethod
    def is_token_blacklisted(token: str) -> bool:
        return redis_client.exists(f"blacklist:{token}") > 0