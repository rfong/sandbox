#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Demo script

import random

from gcounter import GCounter
from pubsub import PubSub


def demo():
    '''Demo gCRDT'''
    ps = PubSub()
    nodes = [GCounter(idx, ps) for idx in range(3)]

    for i in range(10):
        node = random.choice(nodes)
        node.increment()
        for n in nodes:
            print("Node %d says %d" % (n.idx, n.value()))


if __name__ == '__main__':
    demo()
