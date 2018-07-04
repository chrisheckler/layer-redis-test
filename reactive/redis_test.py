from charms.reactive import (
    when,
    when_not,
    set_flag,
    clear_flag,
    endpoint_from_flag,
)

from charmhelpers.core.hookenv import status_set, log
from charmhelpers.core import unitdata

KV = unitdata.kv()


REDIS_OUT = '/home/ubuntu/redis_config.txt'


@when('endpoint.redis.available')
@when_not('snap-db-redis.redis.available')
def get_redis_data():
    """ Get redis data
    """
    KV.set('count', KV.get('count', 0)+1)

    status_set('maintenance', 'Getting redis data')

    endpoint = endpoint_from_flag('endpoint.redis.available')

    with open(REDIS_OUT, 'a') as f:
        f.write(str(endpoint.relation_data()) + "\n")

    status_set('active', str(endpoint.relation_data()))

    log(str(endpoint.relation_data()))
    log("THIS IS  THE {}th time I've ran".format(KV.get('count')))

    set_flag('snap-db-redis.redis.available')
