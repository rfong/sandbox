#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# A simple pub/sub.

import logging
from collections import namedtuple
from typing import Callable

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)


Listener = namedtuple("Listener", ["id", "callable"])

class PubSub(object):
    '''This PubSub unsubscribes listeners if they crash.'''

    def __init__(self, unsub_err_type):
        self.unsub_err_type = unsub_err_type
        self.listeners = []

    def publish(self, **kwargs):
        '''Publish an update to all subscribed listeners.'''
        logger.info("publish: %s" % str(kwargs))
        for listener in self.listeners:
            try:
                listener.callable(**kwargs)
            except self.unsub_err_type as err:
                logger.error(
                    "Node %d crashed, unsubscribing it" % listener.id)
                self.unsubscribe(listener.id)

    def subscribe(self, id, listener: Callable):
        '''Subscribe a listener function with an ID attached.'''
        self.listeners.append(Listener(id, listener))

    def unsubscribe(self, id):
        '''Remove listeners matching this id.'''
        self.listeners = [sub for sub in self.listeners if sub.id is not id]


if __name__ == "__main__":
    '''Quick test'''
    def listener1(x=None):
        print("#1 received x:", x)
    def listener2(**kwargs):
        print("#2 received:", kwargs)

    pubsub = PubSub()
    pubsub.publish(x=1)  # nothing happens

    pubsub.subscribe(listener1)
    pubsub.publish(x=2)

    pubsub.subscribe(listener2)
    pubsub.publish(x=3)

    pubsub.subscribe(listener2)
    pubsub.publish(apple="banana")  # listener1 can't deal w/ it. that's fine
