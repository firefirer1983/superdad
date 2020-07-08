from .bucket import TokenBucket

LIMIT_API_COUNT = 16
limit = TokenBucket(LIMIT_API_COUNT)
