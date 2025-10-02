import psycopg2
import redis
from core.config import Settings
from core.exceptions import InternalServerError


class HealthRepository:
    def __init__(self, settings: Settings):
        self.settings = settings

    def check_postgres(self) -> bool:
        """Check PostgreSQL connection"""
        try:
            print("database url ", self.settings.database_url)
            conn = psycopg2.connect(self.settings.database_url)
            conn.close()
            return True
        except Exception as e:
            raise InternalServerError(f"PostgreSQL connection error: {e}")

    def check_redis(self) -> bool:
        """Check Redis connection"""
        try:
            print("redis url ", self.settings.redis_url)
            r = redis.Redis.from_url(self.settings.redis_url)
            r.ping()
            return True
        except Exception as e:
            raise InternalServerError(f"Redis connection error: {e}")
