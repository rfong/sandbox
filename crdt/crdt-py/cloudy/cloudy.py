#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Wrappers to make our CRDT annoying and glitchy like a cloud instance for
# demo purposes.

from functools import wraps
import logging
import random
import time
import types

from gcounter import GCounter
from pubsub import PubSub


logger = logging.getLogger("main")
logging.basicConfig()
logger.setLevel(logging.INFO)


def wrap_all_public_fns_on_cls(cls, decorator):
    '''For all non-underscore-prefixed functions in `cls`, wrap in decorator'''
    return wrap_some_fns_on_cls(
        cls, decorator, lambda name: not name.startswith("_"))

def wrap_some_fns_on_cls(cls, decorator, fn_name_check):
    '''
    For all functions in `cls` for which `fn_name_check` is True, wrap in
    decorator
    '''
    for name in dir(cls):
        if not fn_name_check(name):
            continue
        attr = getattr(cls, name)
        if type(attr) in [types.FunctionType, types.MethodType]:
            setattr(cls, name, decorator(attr))
    return cls


def random_latency(fn):
    '''A decorator that adds random timeouts to a function call'''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        time.sleep(random.uniform(0.0, 1.0))
        return fn(*args, **kwargs)
    return wrapper

class CloudyPubSub(PubSub):
    '''A subclass of PubSub with random latency on public functions.'''
    pass
wrap_all_public_fns_on_cls(CloudyPubSub, random_latency)


class CloudyException(Exception):
    pass

def chance(p):
    '''Return true with a probability of `p` (float in interval [0.0, 1.0]).'''
    return random.uniform(0.0, 1.0) < p

def randomly_crash_inst_fn(fn):
    '''
    Decorator that makes instance fns randomly "crash" an instance, and be
    unresponsive if their instance is "crashed".
    '''
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        # Random chance of crashing.
        self.random_crash()
        # If uncrashed, run the function as usual.
        if not self.crashed:
            return fn(self, *args, **kwargs)
        # If crashed, raise a Cloudy error.
        raise CloudyException
    return wrapper

class CloudyGCounter(GCounter):
    '''A subclass of GCounter that randomly becomes unresponsive.'''
    CHANCE_OF_CRASH = 0.05

    def __init__(self, *args, **kwargs):
        self.crashed = False
        super().__init__(*args, **kwargs)

    def random_crash(self):
        if chance(self.CHANCE_OF_CRASH):
            self.crashed = True

wrap_some_fns_on_cls(
    CloudyGCounter, randomly_crash_inst_fn,
    lambda name: name in ["increment", "value", "_join"])


if __name__ == "__main__":
    '''Demo some nodes incrementing and publishing to each other'''
    ps = CloudyPubSub()
    nodes = [GCounter(idx, ps) for idx in range(3)]

    for i in range(10):
        node = random.choice(nodes)
        node.increment()
        for n in nodes:
            print("Node %d says %d" % (n.idx, n.value()))

