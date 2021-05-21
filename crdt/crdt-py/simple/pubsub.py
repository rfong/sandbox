#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# A simple pub/sub.

import logging
from collections import namedtuple
from typing import Callable

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)


class PubSub(object):

    def __init__(self):
        self.listeners = []

    def publish(self, **kwargs):
        '''Publish an update to all subscribed listeners.'''
        logger.info("publish: %s" % str(kwargs))
        for listener in self.listeners:
            listener(**kwargs)
    
    def subscribe(self, listener: Callable):
        '''Subscribe a listener function.'''
        self.listeners.append(listener)


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
