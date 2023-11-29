import aioredis
import asyncio

async def connect_to_redis():
    redis = await aioredis.create_redis('redis://localhost', encoding='utf-8')
    return redis

async def main():
    redis = await connect_to_redis()
    print(redis)
async def connect_to_redis_true():
    redis = aioredis.from_url(
        'redis://redis:6379',
        encoding='utf-8',
        decode_responses=True)
    return redis
if __name__ == "__main__":
    asyncio.run(main())