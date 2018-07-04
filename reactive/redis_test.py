from charms.reactive import (
    when,
    when_not,
    set_flag,
    clear_flag,
    endpoint_from_flag,
)

from charmhelpers.core.hookenv import status_set, log
from charmhelpers.core import unitdata

from charms.layer.redis_test import render_flask_secrets


KV = unitdata.kv()


REDIS_OUT = '/home/ubuntu/redis_config.txt'


@when('endpoint.redis.available')
@when_not('snap-db-redis.redis.available')
def get_redis_data():
    """ Get/set redis connection info
    """
    status_set('maintenance', 'Getting redis connection info')

    endpoint = endpoint_from_flag('endpoint.redis.available')

    KV.set('redis_host', endpoint.relation_data()[0]['host'])
    KV.set('redis_port', endpoint.relation_data()[0]['port'])

    status_set('active', "Redis connection info received")

    set_flag('snap-db-redis.redis.available')


@when('snap-db-redis.redis.available')
@when_not('flask-secrets.available')
def render_flask_config():
    render_flask_secrets()
    set_flag('flask-secrets.available')


@when('endpoint.redis.departed')
def clear_redis_availabe():
    clear_flag('snap-db-redis.redis.available')
