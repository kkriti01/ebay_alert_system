import json

from redis import Redis

redis = Redis("localhost")

while True:
    r = redis.blpop(['queue:price-report'], 30)
    print(r)
    if r:
        data = json.loads(r[1])
        print(data)
    else:
        print("pass")
