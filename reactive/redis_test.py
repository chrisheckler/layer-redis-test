from charms.reactive import (
    when,
    when_not,
    set_flag,
    clear_flag,
    endpoint_from_flag,
)

from charmhelpers.core.hookenv import status_set, log

from charmhelpers.core import unitdata


REDIS_OUT = '/home/ubuntu/redis_config.txt'

KV = unitdata.kv()


@when('endpoint.redis.available')
@when_not('snap-db-redis.redis.available')
def get_redis_data():
    """ Get redis data
    """

    status_set('maintenance', 'Getting data')

    endpoint = endpoint_from_flag('endpoint.redis.available')

    with open(REDIS_OUT, 'a') as f:
        f.write(str(endpoint.relation_data()))
    status_set('active', str(endpoint.relation_data()))
    log(str(endpoint.relation_data()))
    set_flag('snap-db-redis.redis.available')


@when('endpoint.redis.broken')
def clear_redis_available_flag():
    clear_flag('snap-db-redis.redis.available')
